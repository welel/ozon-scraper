from scrap.database.models.ozon import OzonReview
from scrap.dto.ozon.review import (
    OzonReviewCreateProperties,
    OzonReviewUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewEntity
from scrap.repositories.ozon.interfaces.review import OzonReviewInterface
from scrap.repositories.sqlalchemy_repo import SqlalchemyRepository


class OzonReviewsRepository(
    SqlalchemyRepository[
        str,
        OzonReviewEntity,
        OzonReviewCreateProperties,
        OzonReviewUpdatableProperties,
    ],
    OzonReviewInterface,
):
    sa_model = OzonReview
    entity_py_model = OzonReviewEntity
