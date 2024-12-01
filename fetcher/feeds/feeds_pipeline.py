from logging import getLogger
from uuid import uuid4

from common.dao import ArticlesDao, FeedsDao
from common.models.articles import Article, Feed
from common.tokenization.tokens_distributor import TokensDistributor
from fetcher.feeds.feed_parser import parse_feed
from fetcher.models.feeds import ParsedFeedEntry
from fetcher.settings import FetcherSettings
import datetime

logger = getLogger(__name__)


class FeedsPipeline:
    def __init__(
        self,
        fetcher_settings: FetcherSettings,
        feed_tokens: TokensDistributor,
        feeds_dao: FeedsDao,
        articles_dao: ArticlesDao,
    ):
        self._fetcher_settings = fetcher_settings
        self._feed_tokens = feed_tokens
        self._feeds_dao = feeds_dao
        self._articles_dao = articles_dao

    async def run(self):
        async for token in self._feed_tokens.generate_tokens(
            self._fetcher_settings.feed_tokens_delay_seconds
        ):
            logger.debug("Parsing feeds with token %s", token)
            for feed in await self._feeds_dao.get_feeds(token=token):
                logger.debug("Parsing feed %s", feed.feed_name)

                await self.process_feed(feed)

    async def process_feed(self, feed: Feed):
        parse_feed_result = await parse_feed(feed.feed_url)

        if parse_feed_result.parsed_feed is None:
            logger.error(
                "Failed to parse feed %s: %s", feed.feed_name, parse_feed_result.comment
            )
        else:
            logger.info(
                "Finished parsing feed %s with %s articles",
                feed.feed_name,
                len(parse_feed_result.parsed_feed.entries),
            )

            for entry in parse_feed_result.parsed_feed.entries:
                await self.process_entry(feed, entry)

    async def process_entry(self, feed: Feed, entry: ParsedFeedEntry):
        entry_id = entry.link.removesuffix("/").split("/")[-1]
        article_key = f"{feed.slug}/{entry_id}"
        article_token = hash(article_key) % self._fetcher_settings.article_tokens
        published = datetime.datetime(
            entry.published_parsed[0],
            entry.published_parsed[1],
            entry.published_parsed[2],
            entry.published_parsed[3],
            entry.published_parsed[4],
            entry.published_parsed[5],
            0,
            tzinfo=datetime.UTC
        )

        article = Article(
            id=uuid4(),
            token=article_token,
            title=entry.title,
            url=entry.link,
            published=published,
            file_key=article_key,
            summary=None,
            full_text=None,
            feed=feed,
            chunks=[],
        )

        await self._articles_dao.put_article(article)
        logger.debug("Fetched article %s from feed %s", article_key, feed.feed_name)
