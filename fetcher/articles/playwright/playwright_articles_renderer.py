from logging import getLogger

from playwright.async_api import Browser
from playwright.async_api import Error as PlaywrightError

from fetcher.articles.articles_renderer import ArticlesRenderer

logger = getLogger(__name__)


class PlaywrightArticlesRenderer(ArticlesRenderer):
    def __init__(self, browser: Browser):
        self._browser = browser

    async def render(self, url: str) -> bytes | None:
        try:
            page = await self._browser.new_page()

            response = await page.goto(url)
            if response is None:
                logger.error("No response for url %s", url)
                return

            if response.ok:
                result = await page.pdf()
                logger.info("Fetched page %s size %s bytes", url, len(result))
                return result

            logger.error(
                "Failed to fetch page %s with status %s, %s",
                url,
                response.status,
                response.text(),
            )
        except PlaywrightError as e:
            logger.error("Error while fetching %s: %s", url, e)
        finally:
            if page:
                await page.close()
