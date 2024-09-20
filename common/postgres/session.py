from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from common.postgres.settings import postgres_settings

engine = create_async_engine(postgres_settings.database_url)
async_session = async_sessionmaker(engine)