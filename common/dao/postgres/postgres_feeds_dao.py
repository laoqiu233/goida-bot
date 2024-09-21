from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from common.dao import FeedsDao
from common.models.articles import Feed
from common.postgres.entities import FeedEntity


class PostgresFeedsDao(FeedsDao):
    def __init__(self, async_session: async_sessionmaker[AsyncSession]) -> None:
        self._async_session = async_session

    async def get_feeds(
        self, token: int | None = None, include_inactive: bool = False
    ) -> list[Feed]:
        stmt = select(FeedEntity)

        if token is not None:
            stmt = stmt.where(FeedEntity.token == token)

        if not include_inactive:
            stmt = stmt.where(FeedEntity.is_active.is_(True))

        async with self._async_session() as session:
            result = await session.scalars(stmt)
            return [Feed.model_validate(entity) for entity in result.all()]

    async def get_feed_by_id(self, feed_id: UUID) -> Feed | None:
        stmt = select(FeedEntity).where(FeedEntity.id == feed_id)

        async with self._async_session() as session:
            result = await session.scalar(stmt)
            return result if result is None else Feed.model_validate(result)
