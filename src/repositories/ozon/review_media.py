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

    def get_to_export(
            self,
            media_type: OzonReviewMediaModel.Type,
            comment_count_ge: int = 0,
            like_count_ge: int = 0,
            limit: int | None = None,
            skip_labeled: bool = False,
    ) -> list[OzonReviewMedia]:
        from database.models.ozon import OzonReview
        from database.models.labling import OzonReviewMediaLabel

        with get_session() as session:
            query = session.query(OzonReviewMediaModel).join(
                OzonReview, OzonReview.uuid == OzonReviewMediaModel.review_uuid
            ).join(
                OzonReviewMediaLabel,
                (
                    OzonReviewMediaLabel.review_media_id
                    == OzonReviewMediaModel.id
                ),
                isouter=True,
            ).filter(
                OzonReviewMediaModel.type == media_type,
                OzonReview.comment_count >= comment_count_ge,
                OzonReview.like_count >= like_count_ge,
            )
            if skip_labeled:
                query = query.filter(
                    OzonReviewMediaLabel.review_media_id.is_(None),
                )
            if limit is not None:
                query = query.limit(limit)
            return [OzonReviewMedia.model_validate(rm) for rm in query]

    def get_next_on_label(self) -> OzonReviewMedia | None:
        """Returns first media review without the label."""
        from database.models.ozon import OzonReview
        from database.models.labling import OzonReviewMediaLabel

        with get_session() as session:
            query = session.query(OzonReviewMediaModel).join(
                OzonReview, OzonReview.uuid == OzonReviewMediaModel.review_uuid
            ).join(
                OzonReviewMediaLabel,
                (
                    OzonReviewMediaLabel.review_media_id
                    == OzonReviewMediaModel.id
                ),
                isouter=True,
            ).filter(
                OzonReviewMediaLabel.review_media_id.is_(None),
            ).order_by(
                OzonReview.like_count.desc(),
            )
            if found := query.first():
                return OzonReviewMedia.model_validate(found)
            return None
