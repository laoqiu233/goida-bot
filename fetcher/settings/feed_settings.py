from pydantic_settings import BaseSettings, SettingsConfigDict


class FeedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    feed_tokens_delay_seconds: float
