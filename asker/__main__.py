import asyncio
from common.postgres.session import make_session
from common.dao import ArticlesDao
from common.dao.postgres import PostgresArticlesDao
from pgpt_python.client import AsyncPrivateGPTApi
from pgpt_python.types import ContextFilter
from common.models.articles import ChunkType, DocumentChunk
from asker.settings import asker_settings

system_prompt = '''В контексте предоставлены актуальные отрывки из новостных статьей, необходимо суммаризировать предоставленные отрывки 
новостных статьей и представить краткий тезис разбитый по пунктам только по предоставленным отрывкам. 
Даже если отрывки не актуальны, все равно не отказывайся от суммаризации и предоставь тезисы'''

async def ask(api: AsyncPrivateGPTApi, articles_dao: ArticlesDao, query: str):
    articles = await articles_dao.get_articles(embedded=True, time_range=24*60*60) # Last 24 hours
    print(f"Нашлось {len(articles)} статьей за последние 24 часа")
    chunks: list[DocumentChunk] = []

    for article in articles:
        for chunk in article.chunks:
            if chunk.chunk_type == ChunkType.FULL_TEXT:
                chunks.append(chunk)

    response = await api.contextual_completions.prompt_completion(
        prompt=query,
        system_prompt=system_prompt,
        use_context=True,
        context_filter=ContextFilter(
            docs_ids=list(map(lambda chunk: chunk.id, chunks))
        ),
        include_sources=True
    )

    message = response.choices[0].message
    sources = response.choices[0].sources
    
    if message is None or sources is None:
        print(f"Невалидный ответ от PGPT: {response}")
        return
    
    print(message.content)
    print("Исходники:")
    
    for i, source in enumerate(sources, 1):
        source_article = None

        for article in articles:
            for chunk in article.chunks:
                if chunk.id == source.document.doc_id:
                    source_article = article
                    break
            else:
                continue
            break

        if source_article is None:
            print(f"{i}. Невалидный исходник: {source}")
        else:
            print(f"{i}. {source_article.title} [{source_article.feed.feed_name}] - {source_article.url}")

async def main():
    async_session = make_session(asker_settings)
    pgpt = AsyncPrivateGPTApi(base_url=asker_settings.pgpt_url)
    dao = PostgresArticlesDao(async_session)
    query = input("Введите ваш запрос (будет выполняться раз в 30 минут):")
    while True:
        await ask(pgpt, dao, query)
        await asyncio.sleep(30 * 60)

if __name__ == "__main__":
    asyncio.run(main())