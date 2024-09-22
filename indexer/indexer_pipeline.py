from logging import getLogger

from common.dao import ArticlesDao
from common.settings import ArticlesSettings
from common.tokenization.tokens_distributor import TokensDistributor
from indexer.article_indexer import Indexer

logger = getLogger(__name__)


class IndexerPipeline:
    def __init__(
        self,
        tokens_distributor: TokensDistributor,
        articles_settings: ArticlesSettings,
        articles_dao: ArticlesDao,
        indexer: Indexer,
    ):
        self._tokens_distributor = tokens_distributor
        self._articles_settings = articles_settings
        self._articles_dao = articles_dao
        self._indexer = indexer

    async def run(self):
        async for token in self._tokens_distributor.generate_tokens(
            self._articles_settings.article_tokens_delay_seconds
        ):
            await self.process_token(token)

    async def process_token(self, token: int):
        articles = await self._articles_dao.get_articles(token=token, embedded=False)
        logger.info("Indexing %s articles in token %s", len(articles), token)

        for article in articles:
            await self._indexer.index_article(article)
