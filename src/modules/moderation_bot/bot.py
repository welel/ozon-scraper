import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session

from config import AppConfig
from database import get_session
from database.models.labling import OzonReviewMediaLabel
from repositories.ozon.review_media import OzonReviewMediaRepo


API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
NUM_LABELS = 5

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
logger = logging.getLogger(AppConfig.logger_prefix + __name__)


def _get_label_keyboard(media_id: str) -> InlineKeyboardMarkup:
    callback_template = "button_{media_id}_{label}"
    buttons = []
    for i in range(1, NUM_LABELS + 1):
        callback_data = callback_template.format(media_id=media_id, label=i)
        buttons.append(
            InlineKeyboardButton(text=str(i), callback_data=callback_data)
        )
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def _send_review_media_on_label(chat_id: int):
    if media := OzonReviewMediaRepo().get_next_on_label():
        keyboard = _get_label_keyboard(media.id)

        if media.type == "image":
            await bot.send_photo(
                chat_id=chat_id,
                photo=str(media.url),
                reply_markup=keyboard,
                caption=media.id,
            )
        else:
            await bot.send_video(
                chat_id=chat_id,
                video=str(media.url),
                reply_markup=keyboard,
                caption=media.id,
            )
    else:
        await asyncio.sleep(60)
        await _send_review_media_on_label(chat_id)


def _create_or_update_label(
        media_id: str, label: int, session: Session
) -> tuple[OzonReviewMediaLabel, bool]:
    """Returns created/updated model and flag - is created."""
    db_label = session.query(OzonReviewMediaLabel).filter(
        OzonReviewMediaLabel.review_media_id == media_id,
    ).first()
    if db_label is None:
        db_label = OzonReviewMediaLabel(review_media_id=media_id, label=label)
        session.add(db_label)
        created = True
    else:
        db_label.label = label
        created = False
    session.commit()
    return db_label, created


@router.message(Command('start'))
async def start_(message: types.Message):
    await _send_review_media_on_label(message.chat.id)


@dp.callback_query(lambda c: c.data.startswith('button_'))
async def process_callback(callback_query: types.CallbackQuery):
    media_id, label = callback_query.data.split('_')[-2:]

    logger.info("Mark %s media as %s", media_id, label)

    with get_session() as session:
        _, created = _create_or_update_label(media_id, int(label), session)

    if created:
        await _send_review_media_on_label(callback_query.message.chat.id)


async def start():
    dp.include_router(router)
    await dp.start_polling(bot)
