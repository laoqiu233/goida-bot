from collections import namedtuple
from logging import getLogger
from uuid import UUID

from pgpt_python.client import AsyncPrivateGPTApi
from pgpt_python.types import ContextFilter

from common.dao import ArticlesDao
from common.models.articles import Article, DocumentChunk, RankedDocumentChunk, ChunkType, RankedArticle

from itertools import groupby

logger = getLogger(__name__)

class SearchService:
    def __init__(self, pgpt: AsyncPrivateGPTApi, articles_dao: ArticlesDao):
        self._pgpt = pgpt
        self._articles_dao = articles_dao

    async def search_all(self, term: str) -> list[RankedArticle]:
        articles = await self._articles_dao.get_articles(embedded=True)
        chunks = []

        for article in articles:
            chunks += [*filter(lambda x: x.chunk_type == ChunkType.SUMMARY, article.chunks)]

        logger.info("Searching for %s with %s chunks", term, len(chunks))

        ranked_chunks = await self.search_chunks(chunks, term)

        article_chunks: dict[UUID, list[RankedDocumentChunk]] = {}
        article_mean_relevance: dict[UUID, float] = {}

        for article_id, chunks in groupby(ranked_chunks, key=lambda chunk: chunk.chunk.article_id):
            article_chunks[article_id] = list(chunks)
            relevance_sum = 0

            for chunk in article_chunks[article_id]:
                relevance_sum += chunk.relevance

            article_mean_relevance[article_id] = relevance_sum / len(article_chunks[article_id])

        logger.info("Search for %s returned %s chunks from %s articles", term, len(ranked_chunks), len(article_chunks))

        sorted_article_ids = list(article_mean_relevance.keys())
        sorted_article_ids.sort(key=article_mean_relevance.__getitem__, reverse=True)

        ranked_articles = []

        for article_id in sorted_article_ids:
            article = await self._articles_dao.get_article_by_id(article_id)

            if article is None:
                logger.warning("Sorted article %s not found", article_id)
                continue

            ranked_articles.append(RankedArticle(
                article=article,
                ranked_chunks=article_chunks[article_id],
                mean_relevance=article_mean_relevance[article_id]
            ))

        return ranked_articles

    async def search_chunks(
        self, chunks: list[DocumentChunk], term: str
    ) -> list[RankedDocumentChunk]:
        chunk_to_article: dict[str, UUID] = {}
        ids = []

        for chunk in chunks:
            chunk_to_article[chunk.id] = chunk.article_id
            ids.append(chunk.id)

        retrieved_chunks = await self._pgpt.context_chunks.chunks_retrieval(
            text=term, context_filter=ContextFilter(docs_ids=ids)
        )
        ranked_chunks = []

        for chunk in retrieved_chunks.data:
            if chunk.document.doc_id not in chunk_to_article:

                logger.warning(
                    "Pgpt returned unexpected chunk %s, file %s page %s",
                    chunk.document.doc_id,
                    (chunk.document.doc_metadata or {}).get(
                        "file_name", "no_file_name"
                    ),
                    (chunk.document.doc_metadata or {}).get(
                        "page_label", "no_page_label"
                    ),
                )
                continue

            article_id = chunk_to_article[chunk.document.doc_id]

            ranked_chunk = RankedDocumentChunk(
                chunk=DocumentChunk(id=chunk.document.doc_id, article_id=article_id, chunk_type=ChunkType.FULL_TEXT),
                relevance=chunk.score,
            )

            ranked_chunks.append(ranked_chunk)

        return ranked_chunks
