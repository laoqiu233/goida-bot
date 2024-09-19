import asyncio
from uuid import UUID, uuid4

from common.dao import FeedsDao
from common.models.articles import Feed
from common.tokenization.impl.static_tokens_distributor import \
    StaticTokensDistributor
from fetcher.feeds import FeedsPipeline
from fetcher.settings import feed_settings_live


class FakeFeedsDao(FeedsDao):
    async def get_feeds(
        self, token: int | None = None, include_inactive: bool = False
    ) -> list[Feed]:
        if token == 0:
            return [
                Feed(
                    id=uuid4(),
                    token=0,
                    name="lenta",
                    main_url="https://lenta.ru",
                    feed_url="https://lenta.ru/rss",
                    is_active=True,
                )
            ]
        else:
            return []

    async def get_feed_by_id(self, id: UUID) -> Feed | None:
        return None


fake_feeds = FakeFeedsDao()
tokens = StaticTokensDistributor(5, set(range(5)))
feeds_pipeline = FeedsPipeline(feed_settings_live, tokens, fake_feeds)

if __name__ == "__main__":
    asyncio.run(feeds_pipeline.run())
