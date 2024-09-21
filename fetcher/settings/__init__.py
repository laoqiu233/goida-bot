from fetcher.settings.articles_settings import ArticlesSettings
from fetcher.settings.feeds_settings import FeedsSettings


class FetcherSettings:
    feeds_settings: FeedsSettings
    articles_settings: ArticlesSettings


fetcher_settings = FetcherSettings()
