from common.settings import PgptSettings, PostgresSettings, TelegramSettings


class BotSettings(PostgresSettings, PgptSettings, TelegramSettings):
    pass


bot_settings = BotSettings()
