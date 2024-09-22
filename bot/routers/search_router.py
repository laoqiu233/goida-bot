from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import (
    BlockQuote,
    Bold,
    TextLink,
    as_line,
    as_numbered_section,
    as_section,
)

from bot.utils import validate_search_term
from common.models.articles import Article
from common.services.search_service import SearchService

router = Router(name="search")


@router.message(Command("search"))
async def search_command(
    message: Message, command: CommandObject, search_service: SearchService
):
    term = command.args

    if term is None:
        await message.answer("Не указан запрос поиска!")
        return

    if not validate_search_term(term):
        await message.answer("Невалидный запрос!")
        return

    result = await search_service.search_all(term)

    await answer_search_result(message, result)


async def answer_search_result(message: Message, articles: list[Article]):
    rendered_articles = []

    for article in articles:
        rendered_articles.append(
            as_section(
                Bold(article.file_key),
                as_line(BlockQuote(article.summary)),
                as_line(
                    TextLink(
                        f"Читать полностью на {article.feed.feed_name}", url=article.url
                    )
                ),
            )
        )

    await message.answer(
        as_numbered_section(
            f"Найдено {len(articles)} результатов", *rendered_articles
        ).as_markdown()
    )
