from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Feed(BaseModel):
    id: UUID
    token: int

    name: str
    main_url: str
    feed_url: str
    is_active: bool


class Article(BaseModel):
    id: UUID
    token: int

    link: str
    file_key: str

    summary: Optional[str]
    full_text: Optional[str]
    is_embedded: bool

    feed: Feed
