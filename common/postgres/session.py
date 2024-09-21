from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.settings.postgres_settings import PostgresSettings


def make_session(settings: PostgresSettings):
    engine = create_async_engine(settings.database_url)
    return async_sessionmaker(engine)
