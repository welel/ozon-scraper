import logging

from sqlalchemy.orm import Session

from config import AppConfig
from db import get_session
from db.models.ozon import OzonReview as DBOzonReview
from dto.ozon_review import (
    CreateOzonReviewProperties,
    OzonReview,
    OzonReviewUpdatableProperties,
)
from .interfaces.ozon_review import OzonReviewInterface


class OzonReviewRepo(OzonReviewInterface):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def _get_from_db_by_reviw_uuid(
            self,
            review_uuid: str,
            session: Session,
    ) -> DBOzonReview | None:
        return session.query(DBOzonReview).filter(
            DBOzonReview.review_uuid == review_uuid,
        ).first()

    def _update_by_schema(
            self,
            db_review: DBOzonReview,
            review: OzonReviewUpdatableProperties,
    ) -> None:
        for field, value in review.model_dump(mode="json").items():
            setattr(db_review, field, value)

    def create(self, review: CreateOzonReviewProperties) -> OzonReview:
        db_product = DBOzonReview(**review.model_dump(mode="json"))
        with get_session() as session:
            session.add(db_product)
            session.commit()
            return OzonReview.model_validate(db_product)

    def create_or_update(
            self,
            review: CreateOzonReviewProperties,
    ) -> OzonReview:
        with get_session() as session:
            db_review = self._get_from_db_by_reviw_uuid(
                review.review_uuid, session
            )
            if db_review is None:
                return self.create(review)
            else:
                self._update_by_schema(
                    db_review,
                    OzonReviewUpdatableProperties.model_validate(
                        review.model_dump(exclude_unset=True),
                    )
                )
                session.commit()
                return OzonReview.model_validate(db_review)
