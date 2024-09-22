import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from pgpt_python.client import AsyncPrivateGPTApi

from bot.routers.search_router import router as search_router
from bot.settings import bot_settings
from common.common_logging import setup_logging
from common.dao.postgres import PostgresArticlesDao
from common.postgres.session import make_session
from common.services.search_service import SearchService


async def main():
    print(bot_settings)

    async_session = make_session(bot_settings)
    articles_dao = PostgresArticlesDao(async_session)
    pgpt = AsyncPrivateGPTApi(base_url=bot_settings.pgpt_url)

    search_service = SearchService(pgpt, articles_dao)

    bot = Bot(
        token=bot_settings.telegram_token,
        default=DefaultBotProperties(
            link_preview_is_disabled=True, parse_mode=ParseMode.MARKDOWN_V2
        ),
    )

    dp = Dispatcher(search_service=search_service)
    dp.include_routers(search_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
