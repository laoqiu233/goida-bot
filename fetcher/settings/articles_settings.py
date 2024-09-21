from common.settings import ConfiguredSettings


class ArticlesSettings(ConfiguredSettings):
    article_tokens_delay_seconds: float
    article_tokens: int
    articles_pdf_path: str
