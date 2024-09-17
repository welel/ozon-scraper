from dataclasses import dataclass
from datetime import datetime

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram.enums.parse_mode import ParseMode

from database import get_session
from database.models import (
    OzonMediaType,
    OzonReview,
    OzonReviewMedia,
    OzonReviewMediaLabel,
    TelegramOzonReviewPost,
)

from ..config import (
    TELEGRAM_API_TOKEN,
    TELEGRAM_CHANNEL_CHAT_ID as CHAT_ID,
    TELEGRAM_CHANNEL_NAME,
)


@dataclass
class Media:
    type: OzonMediaType
    url: str


@dataclass
class Post:
    text: str
    media: list[Media]


class PostService:

    def _get_post(self) -> Post | None:
        now = datetime.now()

        with get_session() as session:
            post = session.query(TelegramOzonReviewPost).filter(
                TelegramOzonReviewPost.is_valid.is_(True),
                TelegramOzonReviewPost.post_at.is_not(None),
                TelegramOzonReviewPost.post_at <= now,
                TelegramOzonReviewPost.posted_at.is_(None),
            ).order_by(
                TelegramOzonReviewPost.post_at,
            ).first()
            if post is None:
                return None
            
            post.posted_at = datetime.now()

            query = session.query(
                OzonReviewMedia, OzonReview
            ).join(
                OzonReview,
                OzonReviewMedia.review_uuid == OzonReview.uuid,
            ).join(
                OzonReviewMediaLabel,
                OzonReviewMediaLabel.review_media_id
                == OzonReviewMedia.id,
            ).filter(
                OzonReview.uuid == post.review_uuid,
                OzonReviewMediaLabel.label >= 3,
            )

            review: OzonReview = None
            media_list = []
            for media, review in query:
                review = review
                media_list.append(Media(type=media.type, url=str(media.url)))

            media_list = list(sorted(  # Place video first
                media_list, key=lambda m: m.type == OzonMediaType.image
            ))

            text = (
                "<b>{name}</b> пишет:\n"
                '"{text}"\n'
                "<b>Код товара</b>: {sku_id}\n\n"
                f"{TELEGRAM_CHANNEL_NAME} - подписывайся"
            )
            if post.admin_comment:
                text = f"<b>{post.admin_comment}</b>\n\n" + text

            if review.user_name:
                name = review.user_name.split()[0]
            else:
                name = "Девушка"

            comment_text = (
                review.comment_text
                or review.advantages_text
                or review.disadvantages_text
                or ":)"
            )

            text = text.format(
                name=name, text=comment_text, sku_id=review.product_sku_id
            )

            session.commit()

            return Post(text=text, media=media_list)

    async def send_post(self) -> None:
        post = self._get_post()
        if post is None:
            print("No post to post")
            return

        props = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token=TELEGRAM_API_TOKEN, default=props)

        if len(post.media) > 1:
            media_group = []
            for media in post.media:
                if media.type == OzonReviewMedia.Type.image:
                    media_group.append(
                        InputMediaPhoto(media=media.url, caption=post.text)
                    )
                else:
                    media_group.append(
                        InputMediaVideo(media=media.url, caption=post.text)
                    )

            await bot.send_media_group(CHAT_ID, media=media_group)

        else:
            media = post.media[0]
            if media.type == OzonReviewMedia.Type.image:
                await bot.send_photo(
                    CHAT_ID, photo=media.url, caption=post.text
                )
            else:
                await bot.send_video(
                    CHAT_ID, video=media.url, caption=post.text
                )
