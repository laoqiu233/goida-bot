import asyncio

from playwright.async_api import async_playwright

from common.common_logging import setup_logging
from common.dao.postgres import PostgresArticlesDao, PostgresFeedsDao
from common.postgres.session import async_session
from common.storage.local import LocalArticlesStorage
from common.tokenization.impl.static_tokens_distributor import StaticTokensDistributor
from fetcher.articles import ArticlesPipeline
from fetcher.articles.articles_fetcher import ArticlesFetcher
from fetcher.articles.playwright import PlaywrightArticlesRenderer
from fetcher.feeds import FeedsPipeline
from fetcher.settings import fetcher_settings


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        feeds_dao = PostgresFeedsDao(async_session)
        articles_dao = PostgresArticlesDao(async_session)
        feeds_tokens = StaticTokensDistributor.linear(fetcher_settings.feed_tokens)
        articles_tokens = StaticTokensDistributor.linear(
            fetcher_settings.article_tokens
        )

        articles_renderer = PlaywrightArticlesRenderer(browser)
        articles_storage = LocalArticlesStorage(fetcher_settings.articles_pdf_path)
        fetcher = ArticlesFetcher(articles_storage, articles_renderer)

        feeds_pipeline = FeedsPipeline(
            fetcher_settings,
            feeds_tokens,
            feeds_dao,
            articles_dao,
        )
        articles_pipeline = ArticlesPipeline(
            fetcher_settings, articles_tokens, articles_dao, fetcher
        )

        feeds_task = asyncio.create_task(feeds_pipeline.run())
        articles_pipeline = asyncio.create_task(articles_pipeline.run())

        await feeds_task
        await articles_pipeline


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
