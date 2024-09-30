import asyncio
import logging

from aiogram import Bot, Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session

from config import AppConfig
from database import get_session
from database.models.labling import OzonReviewMediaLabel
from repositories.ozon.review_media import OzonReviewMediaRepo

from ..config import NUM_LABELS


labling_router = Router(name="labling_router")
logger = logging.getLogger(AppConfig.logger_prefix + __name__)


def _get_label_keyboard(media_id: str) -> InlineKeyboardMarkup:
    callback_template = "button_{media_id}_{label}"

    max_width = 5
    rows = []
    buttons = []
    for i in range(1, NUM_LABELS + 1):
        callback_data = callback_template.format(media_id=media_id, label=i)
        buttons.append(
            InlineKeyboardButton(text=str(i), callback_data=callback_data)
        )
        if i % max_width == 0:
            rows.append(list(buttons))
            buttons.clear()
    if buttons:
        rows.append(buttons)
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _send_review_media_on_label(chat_id: int, bot: Bot):
    if media := OzonReviewMediaRepo().get_next_on_label():
        try:
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
        except Exception:
            logger.exception("Failed to send media %s", media)
            with get_session() as session:
                _create_or_update_label(media.id, 1, session)
            await bot.send_message(
                chat_id, f"Failed to label media {media}, set label 1."
            )
            await _send_review_media_on_label(chat_id, bot)
    else:
        bot.send_message(chat_id, "No media on labling.")
        await asyncio.sleep(60)
        await _send_review_media_on_label(chat_id, bot)


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


@labling_router.message(Command('label'))
async def start_labling(message: types.Message, bot: Bot):
    await _send_review_media_on_label(message.chat.id, bot)


@labling_router.callback_query(lambda c: c.data.startswith('button_'))
async def process_callback(callback_query: types.CallbackQuery, bot: Bot):
    media_id, label = callback_query.data.split('_')[-2:]

    logger.info("Mark %s media as %s", media_id, label)

    with get_session() as session:
        _, created = _create_or_update_label(media_id, int(label), session)

    if created:
        await _send_review_media_on_label(callback_query.message.chat.id, bot)
