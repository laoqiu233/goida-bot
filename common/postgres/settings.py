from pydantic_settings import BaseSettings

class PostgresSettings(BaseSettings):
    database_url: str

postgres_settings = PostgresSettings()