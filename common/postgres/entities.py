from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID
from typing import Optional

class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    token: Mapped[int]
    url: Mapped[str]
    file_key: Mapped[str]

    summary: Mapped[Optional[str]]
    full_text: Mapped[Optional[str]]

    feed_id: Mapped[UUID]