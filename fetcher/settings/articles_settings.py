from common.settings import SharedSettings


class ArticlesSettings(SharedSettings):
    article_tokens_delay_seconds: float
    article_tokens: int
    articles_pdf_path: str
