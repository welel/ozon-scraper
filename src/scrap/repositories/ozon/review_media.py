from scrap.database import get_session
from scrap.database.models.ozon import OzonReview, OzonReviewMedia
from scrap.dto.ozon.review_media import (
    OzonReviewMediaCreateProperties,
    OzonReviewMediaUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewMediaEntity
from scrap.repositories.ozon.interfaces.review_media import (
    OzonReviewMediaInterface,
)
from scrap.repositories.sqlalchemy_repo import SqlalchemyRepository


class OzonReviewMediaRepository(
    SqlalchemyRepository[
        str,
        OzonReviewMediaEntity,
        OzonReviewMediaCreateProperties,
        OzonReviewMediaUpdatableProperties,
    ],
    OzonReviewMediaInterface,
):
    sa_model = OzonReviewMedia
    entity_py_model = OzonReviewMediaEntity

    def get_to_export(
        self,
        media_type: OzonReviewMedia.Type,
        comment_count_ge: int = 0,
        like_count_ge: int = 0,
        limit: int | None = None,
    ) -> list[OzonReviewMediaEntity]:
        with get_session() as session:
            query = (
                session.query(OzonReviewMedia)
                .join(
                    OzonReview, OzonReview.uuid == OzonReviewMedia.review_uuid
                )
                .filter(
                    OzonReviewMedia.type == media_type,
                    OzonReview.comment_count >= comment_count_ge,
                    OzonReview.like_count >= like_count_ge,
                )
            )
            if limit is not None:
                query = query.limit(limit)
            return [self.entity_py_model.model_validate(rm) for rm in query]
