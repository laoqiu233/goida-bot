from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from common.dao import ArticlesDao
from common.models.articles import Article, DocumentChunk
from common.postgres.entities import ArticleEntity, DocumentChunkEntity


class PostgresArticlesDao(ArticlesDao):
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self._async_session = async_session

    async def get_articles(
        self, token: int | None = None, embedded: bool | None = None
    ) -> list[Article]:
        async with self._async_session() as session:
            stmt = (
                select(ArticleEntity)
                .options(selectinload(ArticleEntity.feed))
                .options(selectinload(ArticleEntity.chunks))
            )

            if token is not None:
                stmt = stmt.where(ArticleEntity.token == token)

            if embedded is not None:
                clause = (ArticleEntity.full_text.is_not(None)) & (
                    ArticleEntity.summary.is_not(None)
                )
                if not embedded:
                    clause = ~clause

                stmt = stmt.where(clause)

            result = await session.scalars(stmt)

            return [Article.model_validate(entity) for entity in result.all()]

    async def get_article_by_id(self, article_id: UUID) -> Article | None:
        async with self._async_session() as session:
            stmt = (
                select(ArticleEntity)
                .where(ArticleEntity.id == article_id)
                .options(selectinload(ArticleEntity.feed))
                .options(selectinload(ArticleEntity.chunks))
            )
            result = await session.scalar(stmt)

            return result if result is None else Article.model_validate(result)

    async def get_article_by_url(self, url: str) -> Article | None:
        async with self._async_session() as session:
            stmt = (
                select(ArticleEntity)
                .where(ArticleEntity.url == url)
                .options(selectinload(ArticleEntity.feed))
                .options(selectinload(ArticleEntity.chunks))
            )
            result = await session.scalar(stmt)

            return result if result is None else Article.model_validate(result)

    async def put_article(self, article: Article) -> None:
        if await self.get_article_by_url(article.url) is not None:
            return

        async with self._async_session() as session:
            entity = ArticleEntity(
                id=article.id,
                token=article.token,
                url=article.url,
                file_key=article.file_key,
                summary=article.summary,
                full_text=article.full_text,
                feed_id=article.feed.id,
            )
            session.add(entity)
            await session.commit()

    async def add_chunk(self, document_chunk: DocumentChunk) -> None:
        async with self._async_session() as session:
            entity = DocumentChunkEntity(
                id=document_chunk.id,
                article_id=document_chunk.article_id,
                chunk_type=document_chunk.chunk_type.value,
            )
            session.add(entity)
            await session.commit()

    async def update_summary(self, article_id: UUID, summary: str) -> None:
        async with self._async_session() as session:
            stmt = select(ArticleEntity).where(ArticleEntity.id == article_id)
            entity = await session.scalar(stmt)

            if entity is not None:
                entity.summary = summary
                await session.commit()

    async def update_full_text(self, article_id: UUID, full_text: str) -> None:
        async with self._async_session() as session:
            stmt = select(ArticleEntity).where(ArticleEntity.id == article_id)
            entity = await session.scalar(stmt)

            if entity is not None:
                entity.full_text = full_text
                await session.commit()
