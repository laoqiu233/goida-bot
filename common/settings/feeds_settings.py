from common.settings.configured_settings import ConfiguredSettings


class FeedsSettings(ConfiguredSettings):
    feed_tokens_delay_seconds: float
    feed_tokens: int
