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
        # like = ""
        # unlike = ""
        # with get_session() as session:
        #     query = session.query(DBOzonProduct).filter(
        #         DBOzonProduct.name.ilike(like),
        #         DBOzonProduct.name.not_ilike(unlike),
        #         DBOzonProduct.review_count > 100,
        #     ).order_by(
        #         DBOzonProduct.review_count.desc(),
        #     ).limit(100)
        #     return [OzonProduct.model_validate(prod) for prod in query]
        return
