from scrap.database import get_session
from scrap.database.models.ozon import OzonProduct
from scrap.dto.ozon.product import (
    OzonProductCreateProperties,
    OzonProductUpdatableProperties,
)
from scrap.entities.ozon import OzonProductEntity
from scrap.repositories.ozon.interfaces.product import OzonProductInterface
from scrap.repositories.sqlalchemy_repo import SqlalchemyRepository


class OzonProductsRepository(
        SqlalchemyRepository[
            int,
            OzonProductEntity,
            OzonProductCreateProperties,
            OzonProductUpdatableProperties,
        ],
        OzonProductInterface,
):
    sa_model = OzonProduct
    entity_py_model = OzonProductEntity

    def get_list_on_parsing(self) -> list[OzonProductEntity]:
        with get_session() as session:
            query = session.query(OzonProduct).filter(
                OzonProduct.review_count >= 500,
                # OzonProduct.category_id.in_((...)),
            ).order_by(
                OzonProduct.category_id,
                OzonProduct.review_count.desc(),
            )
            return [
                self.entity_py_model.model_validate(product)
                for product in query
            ]
