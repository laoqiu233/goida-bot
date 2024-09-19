from common.dao import FeedsDao
from common.tokenization.tokens_distributor import TokensDistributor
from fetcher.feeds.feed_parser import parse_feed
from fetcher.settings.feed_settings import FeedSettings


class FeedsPipeline:
    def __init__(
        self,
        feed_settings: FeedSettings,
        feed_tokens: TokensDistributor,
        feeds_dao: FeedsDao,
    ):
        self._feed_settings = feed_settings
        self._feed_tokens = feed_tokens
        self._feeds_dao = feeds_dao

    async def run(self):
        async for token in self._feed_tokens.generate_tokens(
            self._feed_settings.feed_tokens_delay_seconds
        ):
            print(f"Parsing feeds with token {token}")
            for feed in await self._feeds_dao.get_feeds(token=token):
                print(f"Parsing feed {feed.name}")

                parse_feed_result = await parse_feed(feed.feed_url)

                if parse_feed_result.parsed_feed is None:
                    print(f"Failed! {parse_feed_result.comment}")
                else:
                    print(
                        f"Success! Parsed {len(parse_feed_result.parsed_feed.entries)} articles"
                    )
