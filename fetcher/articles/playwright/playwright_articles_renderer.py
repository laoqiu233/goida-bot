from logging import getLogger

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Playwright

from fetcher.articles.articles_renderer import ArticlesRenderer

logger = getLogger(__name__)


class PlaywrightArticlesRenderer(ArticlesRenderer):
    def __init__(self, pw: Playwright):
        self._pw = pw
        self._browser = None
        self._context = None

    async def render(self, url: str) -> bytes | None:
        try:
            if self._browser is None:
                logger.warning("Restarting PW browser")
                self._browser = await self._pw.chromium.launch()

            if self._context is None:
                self._context = await self._browser.new_context()

            page = await self._context.new_page()

            response = await page.goto(url, timeout=0)
            
            if response is None:
                logger.error("No response for url %s", url)
                return
    
            if response.ok:
                result = await page.pdf()
                logger.info("Fetched page %s size %s bytes", url, len(result))
                await page.close()
                return result

            logger.error("Failed to fetch page %s with status %s", url, response.status)

        except PlaywrightError as e:
            logger.error("Error while fetching %s: %s", url, e)