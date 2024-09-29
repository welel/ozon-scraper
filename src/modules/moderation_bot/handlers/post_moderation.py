import logging
import uuid

import sqlalchemy as sa
from aiogram import Bot, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from jinja2 import Template

from config import AppConfig
from database import get_session
from database.models import (
    OzonReview,
    OzonReviewMedia,
    OzonReviewMediaLabel,
    Post,
    PostMedia,
    PostOzonReviewMedia,
    PostPool,
    PostPoolPost,
    PostTemplate,
    PostType,
)
from modules.moderation_bot.config import TELEGRAM_ADMIN_ID


MAX_CAPTION_LEN = 1024


router = Router(name="moderation_router")
storage = MemoryStorage()
logger = logging.getLogger(AppConfig.logger_prefix + __name__)
fill_commnet = State()
_storage = {}


def _get_moderation_keyboard(moderation_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Tier 4", callback_data=f"tier_4_{moderation_id}"
            ),
            InlineKeyboardButton(
                text="Tier 3", callback_data=f"tier_3_{moderation_id}"
            ),
            InlineKeyboardButton(
                text="Tier 2", callback_data=f"tier_2_{moderation_id}"
            ),
            InlineKeyboardButton(
                text="Tier 1", callback_data=f"tier_1_{moderation_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Add comment",
                callback_data=f"add_comment_{moderation_id}",
            ),
            InlineKeyboardButton(
                text="Decline",
                callback_data=f"decline_{moderation_id}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def decline_media(media_list: list[OzonReviewMedia]) -> None:
    delined_marks = []
    for media in media_list:
        delined_marks.append(PostOzonReviewMedia(
            review_media_id=media.id,
            is_decliend=True,
        ))

    with get_session() as session:
        session.add_all(delined_marks)
        session.commit()


async def _send_post_on_review(chat_id: int, bot: Bot):

    with get_session() as session:

        # 1. Find available review for post
        result = session.query(
            OzonReview,
            sa.func.max(OzonReviewMediaLabel.label).label("max_label"),
        ).join(
            OzonReviewMedia, OzonReview.uuid == OzonReviewMedia.review_uuid
        ).join(
            OzonReviewMediaLabel,
            OzonReviewMediaLabel.review_media_id == OzonReviewMedia.id,
        ).outerjoin(
            PostOzonReviewMedia,
            PostOzonReviewMedia.review_media_id == OzonReviewMedia.id,
        ).filter(
            PostOzonReviewMedia.is_decliend.is_(None),
        ).group_by(
            OzonReview.uuid
        ).having(
            sa.func.max(OzonReviewMediaLabel.label) >= 2
        ).order_by(
            sa.func.max(OzonReviewMediaLabel.label).desc()
        ).first()

        if result is None:
            raise ValueError(f"No available review for post: {result}")

        db_review, label = result

        db_media_list = session.query(
            OzonReviewMedia
        ).join(
            OzonReview, OzonReview.uuid == OzonReviewMedia.review_uuid
        ).join(
            OzonReviewMediaLabel,
            OzonReviewMediaLabel.review_media_id == OzonReviewMedia.id,
        ).filter(
            OzonReview.uuid == db_review.uuid,
            OzonReviewMediaLabel.label >= 2,
        ).all()
        db_media_list = list(sorted(  # Place video first
            db_media_list, key=lambda m: m.type == OzonReviewMedia.Type.image
        ))

        # 2. Create post, post media from review, media data

        # 2.1. Render content from the template

        POST_TYPE = "moderation_review"

        db_template = session.query(PostTemplate).join(
            PostType, PostType.post_template_id == PostTemplate.id
        ).filter(
            PostType.name == POST_TYPE
        ).first()

        if db_template is None:
            raise ValueError(f"No template for type : {POST_TYPE}")

        template_params = {
            "review_uuid": db_review.uuid,
            "user_name": db_review.user_name,
            "comment": (
                db_review.comment_text
                or db_review.advantages_text
                or db_review.disadvantages_text
            ),
            "label": label,
        }

        template = Template(db_template.template_content)
        content = template.render(template_params)

        # 2.2. Prepare telegram media

        media_group = []

        for db_media in db_media_list:
            if db_media.type == OzonReviewMedia.Type.image:
                media_group.append(InputMediaPhoto(media=db_media.url))
            else:
                media_group.append(InputMediaVideo(media=db_media.url))

        if not media_group:
            raise ValueError(f"No media group: {media_group}")

        media_group[0].caption = content[:MAX_CAPTION_LEN]

        # 3. Send on moderation

        moderation_id = str(uuid.uuid4())
        _storage[moderation_id] = {"review": db_review, "media": db_media_list}
        keyboard = _get_moderation_keyboard(moderation_id)

        try:
            await bot.send_media_group(chat_id, media=media_group)
            await bot.send_message(
                chat_id, db_review.uuid, reply_markup=keyboard
            )
        except TelegramBadRequest as e:
            logger.error("Failed to send post %s: %s", media_group, e)
            decline_media(db_media_list)


@router.message(Command("p"))
async def start_post_moderation(message: types.Message, bot: Bot):
    if message.from_user.id != TELEGRAM_ADMIN_ID:
        return
    await _send_post_on_review(message.chat.id, bot)


@router.callback_query(
        lambda c: c.data.startswith("add_comment_"),
        StateFilter(default_state),
)
async def handle_add_comment(
        cb: types.CallbackQuery, bot: Bot, state: FSMContext
):
    await bot.send_message(cb.message.chat.id, text="Enter comment:")
    moderation_id = cb.data.split('_')[-1]
    await state.set_state(fill_commnet)
    await state.set_data({"moderation_id": moderation_id})


@router.message(StateFilter(fill_commnet))
async def process_fill_comment(message: Message, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    moderation_id = state_data["moderation_id"]
    await state.clear()
    _storage[moderation_id]["admin_comment"] = message.text
    await bot.send_message(message.chat.id, "Comment added")


@router.callback_query(lambda c: c.data.startswith("tier_"))
async def handle_approve(cb: types.CallbackQuery, bot: Bot):
    tier, moderation_id = cb.data.split('_')[-2:]
    tier = int(tier)

    # 1. Get review, media data, admin comment

    db_review = _storage[moderation_id]["review"]
    db_media_list = _storage[moderation_id]["media"]
    admin_comment = _storage[moderation_id].get("admin_comment")

    # 2. Choose type, pool, template_params

    if db_review.user_name is not None:
        user_name = db_review.user_name.split()[0]
    else:
        user_name = "Девушка"

    comment = (
        db_review.comment_text
        or db_review.advantages_text
        or db_review.disadvantages_text
    )

    template_params = {
        "user_name": user_name,
        "comment": comment,
        "product_id": db_review.product_sku_id,
    }

    if admin_comment and comment:
        POST_TYPE = "review_post_with_admin_comment"
        template_params["admin_comment"] = admin_comment
    elif comment:
        POST_TYPE = "review_post"
    else:
        POST_TYPE = "review_post_without_comment"
        template_params["admin_comment"] = admin_comment
    POOL_NAME = f"tier_{tier}"

    # 3. Create post

    # 3.1. Create post

    with get_session() as session:

        result = session.query(PostType, PostTemplate).join(
            PostType, PostType.post_template_id == PostTemplate.id
        ).filter(
            PostType.name == POST_TYPE
        ).first()

        db_type, db_template = result

        if db_type is None or db_template is None:
            raise ValueError(f"No template or type for : {POST_TYPE}")

        template = Template(db_template.template_content)
        content = template.render(template_params)

        db_post = Post(
            title=f"Review Post - {db_review.uuid}",
            content=content,
            template_params=template_params,
            post_type_id=db_type.id,
            data={
                "review_uuid": db_review.uuid,
                "media": [media.id for media in db_media_list],
            },
        )
        session.add(db_post)
        session.flush()

    # 3.2. Add post media

        db_post_media = []
        for media in db_media_list:
            db_post_media.append(PostMedia(
                type=media.type,
                url=media.url,
                post_id=db_post.id,
            ))
        session.add_all(db_post_media)

    # 4. Put post in the pool

        db_pool = session.query(PostPool).filter(
            PostPool.name == POOL_NAME
        ).first()
        if db_pool is None:
            raise ValueError(f"Pool with name {POOL_NAME} isn't found")

        pool_ref = PostPoolPost(post_id=db_post.id, pool_id=db_pool.id)
        session.add(pool_ref)

    # 5. Mark review media of the post

        marks = []
        for media in db_media_list:
            marks.append(PostOzonReviewMedia(
                post_id=db_post.id, review_media_id=media.id
            ))
        session.add_all(marks)

    # 6. Commit changes

        session.commit()

        await bot.send_message(
            cb.message.chat.id,
            f"Post ({db_post.id}) added to tier {tier}",
        )
    await _send_post_on_review(cb.message.chat.id, bot)


@router.callback_query(lambda c: c.data.startswith("decline_"))
async def handle_decline(cb: types.CallbackQuery, bot: Bot):

    # 1. Get review, media data, admin comment

    moderation_id = cb.data.split('_')[-1]
    db_review = _storage[moderation_id]["review"]
    db_media_list = _storage[moderation_id]["media"]

    # 2. Decline media

    decline_media(db_media_list)

    await bot.send_message(cb.message.chat.id, f"Declined: {db_review.uuid}")
    await _send_post_on_review(cb.message.chat.id, bot)
