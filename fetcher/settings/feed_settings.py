from common.settings import SharedSettings


class FeedSettings(SharedSettings):
    feed_tokens_delay_seconds: float

    feed_tokens: int
    article_tokens: int
