from common.settings import SharedSettings


class PostgresSettings(SharedSettings):
    database_url: str


postgres_settings = PostgresSettings()
