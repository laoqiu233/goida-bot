from itertools import groupby
from logging import getLogger

from pgpt_python.core import ApiError

from common.dao import ArticlesDao
from common.models.articles import Article, ChunkType, DocumentChunk
from common.storage import ArticlesStorage
from indexer.services.embedding import EmbeddingService
from indexer.services.prompting import PromptingService

logger = getLogger(__name__)


class IndexingError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Indexer:
    def __init__(
        self,
        embed: EmbeddingService,
        prompt: PromptingService,
        articles_storage: ArticlesStorage,
        articles_dao: ArticlesDao,
    ):
        self._embed = embed
        self._prompt = prompt
        self._articles_storage = articles_storage
        self._articles_dao = articles_dao

    async def index_article(self, article: Article):
        grouped_chunks = dict(
            groupby(article.chunks, key=lambda chunk: chunk.chunk_type)
        )
        raw_chunks = list(grouped_chunks.get(ChunkType.RAW, []))
        full_text_chunks = list(grouped_chunks.get(ChunkType.FULL_TEXT, []))
        summary_chunks = list(grouped_chunks.get(ChunkType.SUMMARY, []))

        try:
            if len(full_text_chunks) <= 0:
                raw_chunks = await self._embed_raw(article, raw_chunks)
            await self._generate_full_text(article, raw_chunks)
            full_text_chunks = await self._embed_full_text(article, full_text_chunks)
            await self._generate_summary(article, full_text_chunks)
            summary_chunks = await self._embed_summary(article, summary_chunks)
            await self._embed.remove_embeds(raw_chunks)
            for chunk in raw_chunks:
                await self._articles_dao.remove_chunk(chunk)
        except IndexingError as e:
            logger.warning("Failed to index article %s: %s", article.id, e.msg)
        except ApiError as e:
            logger.warning(
                "Got error from pgpt when indexing article %s: %s", article.id, e
            )

    async def _embed_raw(
        self, article: Article, raw_chunks: list[DocumentChunk]
    ) -> list[DocumentChunk]:
        if len(raw_chunks) == 0:
            logger.info(
                "Article %s has no raw chunks, sending to embed", article.file_key
            )

            article_file = await self._articles_storage.read(article.file_key)

            if article_file is None:
                raise IndexingError(f"Article {article.file_key} not found in storage")

            raw_chunks = await self._embed.embed_file(
                article.id, article.file_key, article_file
            )

            logger.info(
                "Generated %s raw chunks for article %s",
                len(raw_chunks),
                article.file_key,
            )

            if len(raw_chunks) == 0:
                raise IndexingError(
                    f"Article {article.file_key} generated no raw chunks"
                )

            for chunk in raw_chunks:
                await self._articles_dao.add_chunk(chunk)

        return raw_chunks

    async def _generate_full_text(
        self, article: Article, raw_chunks: list[DocumentChunk]
    ):
        if article.full_text is not None:
            return

        if len(raw_chunks) == 0:
            raise IndexingError(
                f"Article {article.id} with no raw chunks reach prompting"
            )

        logger.info("Article %s has no full text, prompting", article.file_key)
        full_text = await self._prompt.full_text(article.title, raw_chunks)

        if full_text is None:
            raise IndexingError(
                f"Failed to generate full text for article {article.file_key}"
            )

        logger.info(
            "Generated full text for article %s: %s",
            article.file_key,
            full_text,
        )

        await self._articles_dao.update_full_text(article.id, full_text)
        article.full_text = full_text

    async def _embed_full_text(
        self, article: Article, full_text_chunks: list[DocumentChunk]
    ) -> list[DocumentChunk]:
        if article.full_text is None:
            raise IndexingError(
                f"Article {article.file_key} with no full text reached embedding"
            )

        if len(full_text_chunks) == 0:
            logger.info(
                "Article %s has no full text chunks, sending to embed", article.file_key
            )

            full_text_chunks = await self._embed.embed_full_text(
                article.id, article.file_key, article.full_text
            )

            logger.info(
                "Generated %s full text chunks for article %s",
                len(full_text_chunks),
                article.file_key,
            )

            if len(full_text_chunks) == 0:
                raise IndexingError(
                    f"Article {article.file_key} generated no full text chunks"
                )

            for chunk in full_text_chunks:
                await self._articles_dao.add_chunk(chunk)

        return full_text_chunks

    async def _generate_summary(
        self, article: Article, full_text_chunks: list[DocumentChunk]
    ):
        if article.summary is not None:
            return

        if len(full_text_chunks) == 0:
            raise IndexingError(
                f"Artilce {article.id} with no full text chunks reached prompting"
            )

        logger.info("Article %s has no summary, prompting", article.file_key)
        summary = await self._prompt.summarize(full_text_chunks)

        if summary is None:
            raise IndexingError(
                f"Failed to generate summary for article {article.file_key}"
            )

        logger.info(
            "Generated summary for article %s: %s",
            article.file_key,
            summary,
        )
        await self._articles_dao.update_summary(article.id, summary)
        article.summary = summary

    async def _embed_summary(
        self, article: Article, summary_chunks: list[DocumentChunk]
    ) -> list[DocumentChunk]:
        if article.summary is None:
            raise IndexingError(
                f"Article {article.id} with no summary reached embedding"
            )

        if len(summary_chunks) == 0:
            logger.info(
                "Article %s has no summary chunks, sending to embed", article.file_key
            )

            summary_chunks = await self._embed.embed_summary(
                article.id, article.file_key, article.summary
            )

            logger.info(
                "Generated %s summary chunks for article %s",
                len(summary_chunks),
                article.file_key,
            )

            if len(summary_chunks) == 0:
                raise IndexingError(
                    f"Article {article.file_key} generated no summary chunks"
                )

            for chunk in summary_chunks:
                await self._articles_dao.add_chunk(chunk)

        return summary_chunks
