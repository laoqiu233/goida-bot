from logging import getLogger

from common.dao import ArticlesDao
from common.models.articles import Article
from common.storage import ArticlesStorage
from indexer.services.embedding import EmbeddingService
from indexer.services.prompting import PromptingService

logger = getLogger(__name__)


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
        if len(article.chunks) == 0:
            logger.info("Article %s has no chunks, sending to embed", article.file_key)

            article_file = await self._articles_storage.read(article.file_key)

            if article_file is None:
                logger.warning(
                    "Article %s not found in storage, skipping", article.file_key
                )
                return

            chunks = await self._embed.embed(article.id, article.file_key, article_file)

            if len(chunks) == 0:
                logger.warning(
                    "Embed generated 0 chunks for article %s, skipping",
                    article.file_key,
                )

            logger.info(
                "Generated %s chunks for article %s", len(chunks), article.file_key
            )

            for chunk in chunks:
                await self._articles_dao.add_chunk(chunk)

        else:
            chunks = article.chunks

        if article.summary is None:
            logger.info("Article %s has no summary, prompting", article.file_key)
            summary = await self._prompt.summarize(chunks)

            if summary is None:
                logger.warning(
                    "Failed to generate summary for article %s", article.file_key
                )
            else:
                logger.info(
                    "Generated summary for article %s: %s", article.file_key, summary
                )
                await self._articles_dao.update_summary(article.id, summary)

        if article.full_text is None:
            logger.info("Article %s has no full text, prompting", article.file_key)
            full_text = await self._prompt.full_text(chunks)

            if full_text is None:
                logger.warning(
                    "Failed to generate full text for article %s", article.file_key
                )
            else:
                logger.info(
                    "Generated full text for article %s: %s",
                    article.file_key,
                    full_text,
                )
                await self._articles_dao.update_full_text(article.id, full_text)
