from common.settings import (
    ArticlesSettings,
    FeedsSettings,
    PostgresSettings,
    S3Settings,
)


class FetcherSettings(FeedsSettings, ArticlesSettings, S3Settings, PostgresSettings):
    pass


fetcher_settings = FetcherSettings()
