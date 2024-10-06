from scrap.database import get_session
from scrap.database.models.ozon import OzonReview as OzonReviewModel
from scrap.dto.ozon.review import (
    OzonReview,
    OzonReviewCreateProperties,
    OzonReviewUpdatableProperties,
)

from ..sqlalchemy_repo import SqlalchemyBaseRepo
from .interfaces.review import OzonReviewInterface


class OzonReviewsRepo(SqlalchemyBaseRepo, OzonReviewInterface):
    sa_model = OzonReviewModel
    py_model = OzonReview

    def create(self, review: OzonReviewCreateProperties) -> OzonReview:
        with get_session() as session:
            self._create(review, session)

    def update(
            self,
            uuid: str,
            review: OzonReviewUpdatableProperties,
    ) -> OzonReview:
        with get_session() as session:
            return self._update(uuid, review, session)

    def create_or_update(
            self,
            review: OzonReviewCreateProperties,
    ) -> OzonReview:
        with get_session() as session:
            return self._create_or_update(review.uuid, review, session)

    def get(self, uuid: str) -> OzonReview | None:
        with get_session() as session:
            return self._get(uuid, session)
