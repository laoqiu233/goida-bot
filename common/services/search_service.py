from collections import namedtuple
from logging import getLogger
from uuid import UUID

from pgpt_python.client import AsyncPrivateGPTApi
from pgpt_python.types import ContextFilter

from common.dao import ArticlesDao
from common.models.articles import Article, DocumentChunk, RankedDocumentChunk

logger = getLogger(__name__)
ArticleRelevance = namedtuple("ArticleRelevance", "chunks_count relevance_sum")


class SearchService:
    def __init__(self, pgpt: AsyncPrivateGPTApi, articles_dao: ArticlesDao):
        self._pgpt = pgpt
        self._articles_dao = articles_dao

    async def search_all(self, term: str) -> list[Article]:
        articles = await self._articles_dao.get_articles(embedded=True)
        chunks = []

        for article in articles:
            chunks += article.chunks

        ranked_chunks = await self.search_chunks(chunks, term)

        article_relevances: dict[UUID, ArticleRelevance] = {}

        for chunk in ranked_chunks:
            relevance = article_relevances.get(
                chunk.chunk.article_id, ArticleRelevance(0, 0)
            )
            new_relevance = ArticleRelevance(
                relevance.chunks_count + 1, relevance.relevance_sum + chunk.relevance
            )
            article_relevances[chunk.chunk.article_id] = new_relevance

        sorted_articles_ids = map(
            lambda x: x[0],
            sorted(
                list(article_relevances.items()),
                key=lambda x: x[1].relevance_sum / x[1].chunks_count,
            ),
        )

        articles = []

        for article_id in sorted_articles_ids:
            article = await self._articles_dao.get_article_by_id(article_id)

            if article is None:
                logger.warning("Sorted article %s not found", article_id)
                continue

            articles.append(article)

        return articles

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
                chunk=DocumentChunk(id=chunk.document.doc_id, article_id=article_id),
                relevance=chunk.score,
            )

            logger.info("Got chunk %s, text: %s", ranked_chunk, chunk.text)

            ranked_chunks.append(ranked_chunk)

        return ranked_chunks
