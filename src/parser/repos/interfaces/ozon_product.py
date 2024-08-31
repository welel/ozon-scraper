from abc import ABC, abstractmethod

from dto.ozon_product import (
    CreateOzonProductProperties,
    OzonProduct,
)


class OzonProductInterface(ABC):

    @abstractmethod
    def create(self, product: CreateOzonProductProperties) -> OzonProduct:
        pass

    @abstractmethod
    def create_or_update(
            self,
            product: CreateOzonProductProperties,
    ) -> OzonProduct:
        pass

    @abstractmethod
    def get(self, product_id: int) -> OzonProduct | None:
        pass
