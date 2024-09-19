from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from common.models.articles import Feed


class FeedsDao(ABC):
    @abstractmethod
    async def get_feeds(
        self, token: Optional[int] = None, include_inactive: bool = False
    ) -> list[Feed]:
        pass

    @abstractmethod
    async def get_feed_by_id(self, id: UUID) -> Optional[Feed]:
        pass
