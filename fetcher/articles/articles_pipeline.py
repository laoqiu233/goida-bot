import asyncio
from logging import getLogger

from common.dao import ArticlesDao
from common.models.articles import Article
from common.tokenization.tokens_distributor import TokensDistributor
from fetcher.articles.articles_fetcher import ArticlesFetcher
from fetcher.settings import ArticlesSettings

logger = getLogger(__name__)


class ArticlesPipeline:
    def __init__(
        self,
        articles_settings: ArticlesSettings,
        articles_tokens: TokensDistributor,
        articles_dao: ArticlesDao,
        fetcher: ArticlesFetcher,
    ):
        self._articles_settings = articles_settings
        self._articles_tokens = articles_tokens
        self._articles_dao = articles_dao
        self._fetcher = fetcher

    async def run(self):
        async for token in self._articles_tokens.generate_tokens(
            self._articles_settings.article_tokens_delay_seconds
        ):
            await self.process_token(token)

    async def process_token(self, token: int):
        articles = await self._articles_dao.get_articles(token=token, embedded=False)
        logger.info("Rendering %s articles with token %s", len(articles), token)
        await asyncio.gather(*map(self.process_article, articles))

    async def process_article(self, article: Article):
        await self._fetcher.fetch_and_store(article.url, article.file_key)
