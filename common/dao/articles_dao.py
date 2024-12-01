from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from common.models.articles import Article, DocumentChunk


class ArticlesDao(ABC):
    @abstractmethod
    async def get_articles(
        self, token: Optional[int] = None, embedded: Optional[bool] = None, time_range: Optional[int] = None
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

    @abstractmethod
    async def add_chunk(self, document_chunk: DocumentChunk) -> None:
        pass

    @abstractmethod
    async def remove_chunk(self, document_chunk: DocumentChunk) -> None:
        pass

    @abstractmethod
    async def update_summary(self, article_id: UUID, summary: str) -> None:
        pass

    @abstractmethod
    async def update_full_text(self, article_id: UUID, full_text: str) -> None:
        pass
