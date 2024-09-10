from database import get_session
from database.models.ozon import OzonProduct as OzonProductModel
from dto.ozon.product import (
    OzonProduct,
    OzonProductCreateProperties,
    OzonProductUpdatableProperties,
)
from ..sqlalchemy_base import SqlalchemyBaseRepo
from .interfaces.product import OzonProductInterface


class OzonProductsRepo(SqlalchemyBaseRepo, OzonProductInterface):
    sa_model = OzonProductModel
    py_model = OzonProduct

    def create(self, product: OzonProductCreateProperties) -> OzonProduct:
        with get_session() as session:
            self._create(product, session)

    def update(
            self,
            sku_id: int,
            product: OzonProductUpdatableProperties,
    ) -> OzonProduct:
        with get_session() as session:
            return self._update(sku_id, product, session)

    def create_or_update(
            self,
            product: OzonProductCreateProperties,
    ) -> OzonProduct:
        with get_session() as session:
            return self._create_or_update(product.sku_id, product, session)

    def get(self, sku_id: int) -> OzonProduct | None:
        with get_session() as session:
            return self._get(sku_id, session)

    def get_list_on_parsing(self) -> list[OzonProduct]:
        with get_session() as session:
            query = session.query(OzonProductModel).filter(
                OzonProductModel.review_count > 500,
            ).order_by(
                OzonProductModel.review_count.desc(),
            )
            return [OzonProduct.model_validate(prod) for prod in query]
