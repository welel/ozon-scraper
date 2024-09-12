from aiogram import Bot, Dispatcher

from .config import API_TOKEN
from .handlers.labling import labling_router
from .handlers.post_moderation import post_moderation_router


async def start_bot():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(labling_router)
    dp.include_router(post_moderation_router)
    await dp.start_polling(bot)
