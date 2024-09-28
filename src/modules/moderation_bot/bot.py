from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from .config import TELEGRAM_API_TOKEN
from .handlers.labling import labling_router
from .handlers.post_moderation import router as moderation_router


async def start_bot():
    bot = Bot(
        token=TELEGRAM_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(labling_router)
    dp.include_router(moderation_router)
    await dp.start_polling(bot)
