from common.settings import ConfiguredSettings


class PostgresSettings(ConfiguredSettings):
    database_url: str


postgres_settings = PostgresSettings()
