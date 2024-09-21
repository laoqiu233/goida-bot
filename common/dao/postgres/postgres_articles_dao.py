from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from common.dao import ArticlesDao
from common.models.articles import Article
from common.postgres.entities import ArticleEntity


class PostgresArticlesDao(ArticlesDao):
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self._async_session = async_session

    async def get_articles(
        self, token: int | None = None, embedded: bool | None = None
    ) -> list[Article]:
        async with self._async_session() as session:
            stmt = select(ArticleEntity)

            if token is not None:
                stmt = stmt.where(ArticleEntity.token == token).options(
                    selectinload(ArticleEntity.feed)
                )

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
            )
            result = await session.scalar(stmt)

            return result if result is None else Article.model_validate(result)

    async def get_article_by_url(self, url: str) -> Article | None:
        async with self._async_session() as session:
            stmt = (
                select(ArticleEntity)
                .where(ArticleEntity.url == url)
                .options(selectinload(ArticleEntity.feed))
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
