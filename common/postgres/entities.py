from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class FeedEntity(Base):
    __tablename__ = "feeds"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    token: Mapped[int]

    feed_name: Mapped[str]
    slug: Mapped[str]
    main_url: Mapped[str]
    feed_url: Mapped[str]
    is_active: Mapped[bool]


class ArticleEntity(Base):
    __tablename__ = "articles"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    token: Mapped[int]
    url: Mapped[str]
    file_key: Mapped[str]

    summary: Mapped[Optional[str]]
    full_text: Mapped[Optional[str]]

    feed_id: Mapped[UUID] = mapped_column(ForeignKey("feeds.id"))
    feed: Mapped[FeedEntity] = relationship()
    chunks: Mapped[list["DocumentChunkEntity"]] = relationship()


class DocumentChunkEntity(Base):
    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(primary_key=True)
    article_id: Mapped[UUID] = mapped_column(ForeignKey("articles.id"))
