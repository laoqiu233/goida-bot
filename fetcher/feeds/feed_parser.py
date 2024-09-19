from io import BytesIO

import feedparser
import httpx
from pydantic import ValidationError

from fetcher.models.feeds import ParsedFeed, ParseFeedResult


async def parse_feed(feed_url: str) -> ParseFeedResult:
    async with httpx.AsyncClient() as client:
        resp = await client.get(feed_url)

    if resp.status_code != httpx.codes.OK:
        return ParseFeedResult(
            parsed_feed=None,
            comment=f"Feed requets failed with status {resp.status_code}: {resp.text}",
        )

    raw_parsed_feed = feedparser.parse(BytesIO(resp.content))
    try:
        parsed_feed = ParsedFeed.model_validate(raw_parsed_feed)
        return ParseFeedResult(parsed_feed=parsed_feed, comment="")
    except ValidationError as err:
        return ParseFeedResult(parsed_feed=None, comment=f"Failed to parse feed: {err}")
