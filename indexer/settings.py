from common.settings import ArticlesSettings, PgptSettings, PostgresSettings, S3Settings


class IndexerSettings(ArticlesSettings, PgptSettings, PostgresSettings, S3Settings):
    pass


indexer_settings = IndexerSettings()
