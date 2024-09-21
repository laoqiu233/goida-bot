from common.settings.configured_settings import ConfiguredSettings


class PostgresSettings(ConfiguredSettings):
    database_url: str
