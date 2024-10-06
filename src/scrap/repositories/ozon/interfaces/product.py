from abc import ABC, abstractmethod

from dto.ozon.product import (
    OzonProduct,
    OzonProductCreateProperties,
    OzonProductUpdatableProperties,
)


class OzonProductInterface(ABC):

    @abstractmethod
    def create(self, product: OzonProductCreateProperties) -> OzonProduct:
        pass

    @abstractmethod
    def update(
            self,
            sku_id: int,
            product: OzonProductUpdatableProperties,
    ) -> OzonProduct:
        pass

    @abstractmethod
    def create_or_update(
            self,
            product: OzonProductCreateProperties,
    ) -> OzonProduct:
        pass

    @abstractmethod
    def get(self, sku_id: int) -> OzonProduct | None:
        pass
