import logging

from aiogram import Bot, Router, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import AppConfig
from database import _session
from database.models import OzonReviewMedia

from ..services.moderation import PostModerationService


post_moderation_router = Router(name="post_moderation_router")
storage = MemoryStorage()
logger = logging.getLogger(AppConfig.logger_prefix + __name__)
moderation = PostModerationService()
post_gen = moderation.get_post_on_moderation(_session())
fill_commnet = State()


def _get_moderation_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Add comment", callback_data="add_comment"),
        InlineKeyboardButton(text="Approve", callback_data="approve"),
        InlineKeyboardButton(text="Decline", callback_data="decline"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def _send_post_on_review(chat_id: int, bot: Bot):

    try:
        post = next(post_gen)
    except StopIteration:
        await bot.send_message(chat_id, "No posts on moderatoin.")
        return

    keyboard = _get_moderation_keyboard()

    if len(post.media) > 1:
        media_group = []
        for media in post.media:
            if media.type == OzonReviewMedia.Type.image:
                media_group.append(types.InputMediaPhoto(media=str(media.url)))
            else:
                media_group.append(types.InputMediaVideo(media=str(media.url)))
        await bot.send_media_group(
            chat_id, media=media_group, reply_markup=keyboard
        )

    else:
        media = post.media[0]
        if media.type == OzonReviewMedia.Type.image:
            await bot.send_photo(
                chat_id, photo=str(media.url), reply_markup=keyboard
            )
        else:
            await bot.send_video(
                chat_id, video=str(media.url), reply_markup=keyboard
            )


@post_moderation_router.message(Command('post'))
async def start_post_moderation(message: types.Message, bot: Bot):
    await _send_post_on_review(message.chat.id, bot)


@post_moderation_router.callback_query(
        lambda c: c.data == "add_comment", StateFilter(default_state)
)
async def handle_add_comment(
        cb: types.CallbackQuery, bot: Bot, state: FSMContext
):
    await bot.send_message(cb.message.chat.id, text="Enter comment:")
    await state.set_state(fill_commnet)


@post_moderation_router.message(StateFilter(fill_commnet))
async def process_fill_comment(message: Message, bot: Bot, state: FSMContext):
    moderation.set_comment(message.text)
    await state.clear()
    await bot.send_message(message.chat.id, "Commend added")


@post_moderation_router.callback_query(lambda c: c.data == "approve")
async def handle_approve(cb: types.CallbackQuery, bot: Bot):
    moderation.approve()
    await bot.send_message(cb.message.chat.id, "Approved")
    await _send_post_on_review(cb.message.chat.id, bot)


@post_moderation_router.callback_query(lambda c: c.data == "decline")
async def handle_decline(cb: types.CallbackQuery, bot: Bot):
    moderation.decline()
    await bot.send_message(cb.message.chat.id, "Declined")
    await _send_post_on_review(cb.message.chat.id, bot)
