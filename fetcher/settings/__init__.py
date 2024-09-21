from fetcher.settings.articles_settings import ArticlesSettings
from fetcher.settings.feeds_settings import FeedsSettings


class FetcherSettings(FeedsSettings, ArticlesSettings):
    pass


fetcher_settings = FetcherSettings()
