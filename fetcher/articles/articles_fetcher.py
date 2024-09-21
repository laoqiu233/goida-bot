from logging import getLogger

from common.storage import ArticlesStorage
from fetcher.articles.articles_renderer import ArticlesRenderer

logger = getLogger(__name__)


class ArticlesFetcher:
    def __init__(self, storage: ArticlesStorage, renderer: ArticlesRenderer):
        self._storage = storage
        self._renderer = renderer

    async def fetch_and_store(self, url: str, file_key: str):
        if await self._storage.exists(file_key):
            logger.debug("Article %s already stored, skipping", file_key)
            return

        rendered_article = await self._renderer.render(url)

        if rendered_article is None:
            logger.warning("Article %s failed to render", file_key)
            return

        await self._storage.store(file_key, rendered_article)
        logger.info("Finished processing of article %s", file_key)
