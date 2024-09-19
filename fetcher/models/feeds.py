from typing import Optional

from pydantic import BaseModel, ConfigDict


class ParsedFeedEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    link: str


class ParsedFeed(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    entries: list[ParsedFeedEntry]


class ParseFeedResult(BaseModel):
    parsed_feed: Optional[ParsedFeed]
    comment: str
