import logging
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto, InputMediaVideo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import AppConfig
from database import get_session
from database.models.telegram import (
    Channel,
    Post,
    PostMedia,
    PostPoolPost,
    PostSchedulerTrigger,
    PostType,
    Weekday,
)
from modules.moderation_bot.config import TELEGRAM_API_TOKEN


MAX_CAPTION_LEN = 1024


_session = AiohttpSession()
logger = logging.getLogger(AppConfig.logger_prefix + __name__)


async def post_job(
        channel_id: int, post_type_id: int, post_pool_id: int
) -> None:
    logger.info(f"[post_job]: {channel_id=} {post_type_id=} {post_pool_id=}")

    with get_session() as session:

        db_channel = session.query(Channel).filter(
            Channel.id == channel_id
        ).first()

        if db_channel is None:
            logger.warning("Channel with ID %s isn't found", channel_id)
            return

        db_post_type = session.query(PostType).filter(
            PostType.id == post_type_id
        ).first()

        if db_post_type is None:
            logger.error("Wrong post type. Type %s isn't found", post_type_id)
            return

        result = session.query(Post, PostPoolPost).join(
            PostPoolPost, PostPoolPost.post_id == Post.id
        ).filter(
            PostPoolPost.posted_at.is_(None),
            PostPoolPost.pool_id == post_pool_id,
        ).order_by(
            PostPoolPost.order,
        ).first()

        if result is None:
            logger.warning(
                f"Pool is empty {post_type_id=}, {post_pool_id=}, "
                "getting next type..."
            )
            next_type_map = {
                "review_post_with_admin_comment": "review_post",
                "review_post": "review_post_without_comment",
            }
            next_type = next_type_map.get(db_post_type.name)
            if next_type is None:
                logger.warning("Pool is empty")
                return

            db_post_type = session.query(PostType).filter(
                PostType.name == next_type
            ).first()

            if db_post_type is None:
                logger.error(
                    "Wrong next post type. Type %s isn't found", post_type_id
                )
                return

            await post_job(channel_id, db_post_type.id, post_pool_id)

        post, ref = result

        db_media_list = session.query(PostMedia).filter(
            PostMedia.post_id == post.id
        ).all()

        media_group = []

        for db_media in db_media_list:
            if db_media.type == PostMedia.Type.image:
                media_group.append(InputMediaPhoto(media=db_media.url))
            else:
                media_group.append(InputMediaVideo(media=db_media.url))

        if not media_group:
            logger.warning("No media group: %s", media_group)
            return

        media_group[0].caption = post.content[:MAX_CAPTION_LEN]

        bot = Bot(
            token=TELEGRAM_API_TOKEN,
            session=_session,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        await bot.send_media_group(db_channel.chat_id, media=media_group)

        ref.posted_at = datetime.now()
        session.commit()

    logger.info(
        f"[post_job]: {channel_id=} {post_type_id=} {post_pool_id=} posted"
    )


def get_next_weekday_time(
        target_weekday: Weekday,
        hour: int,
        minute: int,
        start_date: datetime | None = None,
) -> datetime:

    if start_date is None:
        start_date = datetime.now()

    current_weekday_num = start_date.weekday()

    # Calculate the difference in days
    days_ahead = (target_weekday.index - current_weekday_num + 7) % 7

    # If the target weekday is today but the time has already passed,
    # move to the next week
    if (
        days_ahead == 0
        and (
            start_date.hour > hour
            or (start_date.hour == hour and start_date.minute >= minute)
        )
    ):
        days_ahead = 7

    next_target_date = start_date + timedelta(days=days_ahead)
    next_target_date = next_target_date.replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )

    return next_target_date


def init_scheudler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    with get_session() as session:
        db_triggers = session.query(PostSchedulerTrigger).all()

        for trigger in db_triggers:
            for weekday in trigger.weekdays:

                start_date = get_next_weekday_time(
                    weekday, trigger.time.hour, trigger.time.minute
                )
                scheduler.add_job(
                    post_job,
                    args=(
                        trigger.channel_id,
                        trigger.post_type_id,
                        trigger.post_pool_id,
                    ),
                    trigger=IntervalTrigger(weeks=1, start_date=start_date),
                )
        # debug job
        # scheduler.add_job(
        #     post_job,
        #     args=(1, 4, 2),
        #     trigger=IntervalTrigger(seconds=30, start_date=datetime.now()),
        # )
    return scheduler
