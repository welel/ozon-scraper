from dataclasses import dataclass
from datetime import datetime
from typing import Generator

import sqlalchemy as sa
from sqlalchemy.orm import Session, Query

from database.models import (
    OzonReview as OzonReviewModel,
    OzonReviewMedia as OzonReviewMediaModel,
    OzonReviewMediaLabel as OzonReviewMediaLabelModel,
    TelegramOzonReviewPost,
)
from dto.ozon.review import OzonReview
from dto.ozon.review_media import OzonReviewMedia

from .post_scheduler import post_scheduler


@dataclass
class Post:
    review: OzonReview
    media: list[OzonReviewMedia]


class PostModerationService:
    _current_post = None
    _current_db_post = None

    def _get_review_uuid_without_post(self) -> str | None:
        query = self._session.query(OzonReviewModel.uuid).join(
            OzonReviewMediaModel,
            OzonReviewMediaModel.review_uuid == OzonReviewModel.uuid,
        ).outerjoin(
            OzonReviewMediaLabelModel,
            OzonReviewMediaLabelModel.review_media_id
            == OzonReviewMediaModel.id,
        ).outerjoin(
            TelegramOzonReviewPost,
            TelegramOzonReviewPost.review_uuid == OzonReviewModel.uuid,
        ).filter(
            # Doesn't have post yet
            TelegramOzonReviewPost.id.is_(None),
        ).group_by(
            OzonReviewModel.uuid,
        ).having(
            # All media are labeled
            sa.func.sum(sa.case(
                (OzonReviewMediaLabelModel.label.is_(None), 1), else_=0
            )) == 0,
            sa.func.max(OzonReviewMediaLabelModel.label) >= 3,
        )
        if row := query.first():
            return row[0]
        return None

    def _get_review_media_query(self, review_uuid: str) -> Query:
        query = self._session.query(
            OzonReviewMediaModel, OzonReviewModel
        ).join(
            OzonReviewModel,
            OzonReviewMediaModel.review_uuid == OzonReviewModel.uuid,
        ).join(
            OzonReviewMediaLabelModel,
            OzonReviewMediaLabelModel.review_media_id
            == OzonReviewMediaModel.id,
        ).filter(
            OzonReviewModel.uuid == review_uuid,
            OzonReviewMediaLabelModel.label >= 3,
        )
        return query

    def get_post_on_moderation(
            self, session: Session
    ) -> Generator[Post, None, None]:
        self._session = session

        while review_uuid := self._get_review_uuid_without_post():
            query = self._get_review_media_query(review_uuid)

            review = None
            media_list = []
            for media, review in query:
                media_list.append(OzonReviewMedia.model_validate(media))
                review = review

            if len(media_list) <= 0:
                continue

            review = OzonReview.model_validate(review)
            media_list = list(sorted(  # Place video first
                media_list,
                key=lambda m: m.type == OzonReviewMediaModel.Type.image,
            ))

            self._current_post = Post(review=review, media=media_list)
            self._current_db_post = TelegramOzonReviewPost(
                review_uuid=review_uuid,
            )
            self._session.add(self._current_db_post)
            yield self._current_post
        self._session.close()

    def set_comment(self, comment: str) -> None:
        self._current_db_post.admin_comment = comment

    def approve(self) -> None:
        last_post = self._session.query(TelegramOzonReviewPost).filter(
            TelegramOzonReviewPost.post_at.is_not(None),
        ).order_by(
            TelegramOzonReviewPost.post_at.desc(),
        ).first()

        if last_post and last_post.post_at:
            next_post_at = post_scheduler.get_next_post_time(last_post.post_at)
        else:
            next_post_at = post_scheduler.get_next_post_time(datetime.now())

        self._current_db_post.post_at = next_post_at
        self._current_db_post.is_valid = True
        self._session.commit()

    def decline(self) -> None:
        self._current_db_post.is_valid = False
        self._session.commit()
