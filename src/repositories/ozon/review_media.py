from database import get_session
from database.models.ozon import OzonReviewMedia as OzonReviewMediaModel
from dto.ozon.review_media import (
    OzonReviewMedia,
    OzonReviewMediaCreateProperties,
    OzonReviewMediaUpdatableProperties,
)
from ..sqlalchemy_base import SqlalchemyBaseRepo
from .interfaces.review_media import OzonReviewMediaInterface


class OzonReviewMediaRepo(SqlalchemyBaseRepo, OzonReviewMediaInterface):
    sa_model = OzonReviewMediaModel
    py_model = OzonReviewMedia

    def create(
            self,
            review_media: OzonReviewMediaCreateProperties,
    ) -> OzonReviewMedia:
        with get_session() as session:
            self._create(review_media, session)

    def update(
            self,
            id_: str,
            review_media: OzonReviewMediaUpdatableProperties,
    ) -> OzonReviewMedia:
        with get_session() as session:
            return self._update(id_, review_media, session)

    def create_or_update(
            self,
            review_media: OzonReviewMediaCreateProperties,
    ) -> OzonReviewMedia:
        with get_session() as session:
            return self._create_or_update(
                review_media.id, review_media, session
            )

    def get(self, id_: str) -> OzonReviewMedia | None:
        with get_session() as session:
            return self._get(id_, session)
