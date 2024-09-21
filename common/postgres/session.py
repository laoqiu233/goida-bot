from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.postgres.settings import postgres_settings

engine = create_async_engine(postgres_settings.database_url)
async_session = async_sessionmaker(engine)
