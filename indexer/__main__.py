import asyncio

from pgpt_python.client import AsyncPrivateGPTApi

from common.common_logging import setup_logging
from common.dao.postgres import PostgresArticlesDao
from common.postgres.session import make_session
from common.storage.local import LocalArticlesStorage
from common.storage.s3 import S3ArticlesStorage
from common.tokenization.impl.static_tokens_distributor import StaticTokensDistributor
from indexer.article_indexer import Indexer
from indexer.indexer_pipeline import IndexerPipeline
from indexer.services.embedding import EmbeddingService
from indexer.services.prompt_storage import PromptStorage
from indexer.services.prompting import PromptingService
from indexer.settings import indexer_settings


async def main():
    pgpt_client = AsyncPrivateGPTApi(base_url=indexer_settings.pgpt_url)

    embed = EmbeddingService(pgpt_client)
    prompt_storage = PromptStorage()
    prompt = PromptingService(pgpt_client, prompt_storage)

    async_session = make_session(indexer_settings)
    articles_dao = PostgresArticlesDao(async_session)

    if indexer_settings.s3_enabled:
        articles_storage = S3ArticlesStorage(indexer_settings)
    else:
        articles_storage = LocalArticlesStorage(indexer_settings.articles_pdf_path)

    articles_tokens = StaticTokensDistributor.linear(indexer_settings.article_tokens)
    indexer = Indexer(embed, prompt, articles_storage, articles_dao)

    indexer_pipeline = IndexerPipeline(
        articles_tokens, indexer_settings, articles_dao, indexer
    )

    await indexer_pipeline.run()


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
