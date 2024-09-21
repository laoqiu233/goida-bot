from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from common.models.articles import Article


class ArticlesDao(ABC):
    @abstractmethod
    async def get_articles(
        self, token: Optional[int] = None, embedded: Optional[bool] = None
    ) -> list[Article]:
        pass

    @abstractmethod
    async def get_article_by_id(self, article_id: UUID) -> Optional[Article]:
        pass

    @abstractmethod
    async def get_article_by_url(self, url: str) -> Optional[Article]:
        pass

    @abstractmethod
    async def put_article(self, article: Article) -> None:
        pass
