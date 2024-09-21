import asyncio

from common.dao.postgres import PostgresArticlesDao, PostgresFeedsDao
from common.common_logging import setup_logging
from common.postgres.session import async_session
from common.tokenization.impl.static_tokens_distributor import \
    StaticTokensDistributor
from fetcher.feeds import FeedsPipeline
from fetcher.settings import feed_settings_live

fake_feeds = PostgresFeedsDao(async_session)
articles_dao = PostgresArticlesDao(async_session)
tokens = StaticTokensDistributor(5, set(range(5)))
feeds_pipeline = FeedsPipeline(feed_settings_live, tokens, fake_feeds, articles_dao)

if __name__ == "__main__":
    setup_logging()
    asyncio.run(feeds_pipeline.run())
