from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Feed(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    token: int

    feed_name: str
    slug: str
    main_url: str
    feed_url: str
    is_active: bool


class Article(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    token: int

    url: str
    file_key: str

    summary: Optional[str]
    full_text: Optional[str]
    chunks: list["DocumentChunk"]

    feed: Feed


class DocumentChunk(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    article_id: UUID


class RankedDocumentChunk(BaseModel):
    chunk: DocumentChunk
    relevance: float


class RankedArticles(BaseModel):
    article: Article
    relevance: float
