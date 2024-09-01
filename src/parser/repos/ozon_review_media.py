import logging

from sqlalchemy.orm import Session

from config import AppConfig
from db import get_session
from db.models.ozon import OzonReviewMedia as DBOzonReviewMedia
from dto.ozon_review_media import (
    CreateOzonReviewMediaProperties,
    OzonReviewMedia,
    OzonReviewMediaUpdatableProperties,
)
from .interfaces.ozon_review_media import OzonReviewMediaInterface


class OzonReviewMediaRepo(OzonReviewMediaInterface):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def _get_from_db_by_url(
            self,
            url: str,
            session: Session,
    ) -> DBOzonReviewMedia | None:
        return session.query(DBOzonReviewMedia).filter(
            DBOzonReviewMedia.url == url,
        ).first()

    def _update_by_schema(
            self,
            db_review: DBOzonReviewMedia,
            review_media: OzonReviewMediaUpdatableProperties,
    ) -> None:
        for field, value in review_media.model_dump(mode="json").items():
            setattr(db_review, field, value)

    def create(
            self,
            review_media: CreateOzonReviewMediaProperties,
    ) -> OzonReviewMedia:
        db_product = DBOzonReviewMedia(**review_media.model_dump(mode="json"))
        with get_session() as session:
            session.add(db_product)
            session.commit()
            return OzonReviewMedia.model_validate(db_product)

    def create_or_update(
            self,
            review_media: CreateOzonReviewMediaProperties,
    ) -> OzonReviewMedia:
        with get_session() as session:
            db_review = self._get_from_db_by_url(
                str(review_media.url), session
            )
            if db_review is None:
                return self.create(review_media)
            else:
                self._update_by_schema(
                    db_review,
                    OzonReviewMediaUpdatableProperties.model_validate(
                        review_media.model_dump(exclude_unset=True),
                    )
                )
                session.commit()
                return OzonReviewMedia.model_validate(db_review)
