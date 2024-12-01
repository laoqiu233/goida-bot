from common.settings import PostgresSettings, PgptSettings

class AskerSettings(PostgresSettings, PgptSettings):
    pass

asker_settings = AskerSettings()