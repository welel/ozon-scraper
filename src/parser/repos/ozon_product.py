import logging

from sqlalchemy.orm import Session

from config import AppConfig
from db import get_session
from db.models.ozon import OzonProduct as DBOzonProduct
from dto.ozon_product import (
    CreateOzonProductProperties,
    OzonProduct,
    OzonProductUpdatableProperties,
)
from .interfaces.ozon_product import OzonProductInterface


class OzonProductsRepo(OzonProductInterface):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def _get_from_db_by_sku_id(
            self,
            sku_id: int,
            session: Session,
    ) -> DBOzonProduct | None:
        return session.query(DBOzonProduct).filter(
            DBOzonProduct.sku_id == sku_id,
        ).first()

    def _update_by_schema(
            self,
            db_product: DBOzonProduct,
            product: OzonProductUpdatableProperties,
    ) -> None:
        for field, value in product.model_dump(mode="json").items():
            setattr(db_product, field, value)

    def create(self, product: CreateOzonProductProperties) -> OzonProduct:
        db_product = DBOzonProduct(**product.model_dump(mode="json"))
        with get_session() as session:
            session.add(db_product)
            session.commit()
            return OzonProduct.model_validate(db_product)

    def create_or_update(
            self,
            product: CreateOzonProductProperties,
    ) -> OzonProduct:
        with get_session() as session:
            db_product = self._get_from_db_by_sku_id(product.sku_id, session)
            if db_product is None:
                return self.create(product)
            else:
                self._update_by_schema(
                    db_product,
                    OzonProductUpdatableProperties.model_validate(
                        product.model_dump(exclude_unset=True),
                    )
                )
                session.commit()
                return OzonProduct.model_validate(db_product)

    def get(self, product_id: int) -> OzonProduct | None:
        with get_session() as session:
            db_product = session.query(DBOzonProduct).filter(
                DBOzonProduct.id == product_id,
            ).first()
            if db_product is not None:
                return OzonProduct.model_validate(db_product)

    def get_list_on_parsing(self) -> list[OzonProduct]:
        like = ""
        unlike = ""
        with get_session() as session:
            query = session.query(DBOzonProduct).filter(
                DBOzonProduct.name.ilike(like),
                DBOzonProduct.name.not_ilike(unlike),
                DBOzonProduct.review_count > 100,
            ).order_by(
                DBOzonProduct.review_count.desc(),
            ).limit(100)
            return [OzonProduct.model_validate(prod) for prod in query]
