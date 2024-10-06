from abc import ABC, abstractmethod

from scrap.dto.ozon.product import (
    OzonProductCreateProperties,
    OzonProductUpdatableProperties,
)
from scrap.entities.ozon import OzonProductEntity


class OzonProductInterface(ABC):

    @abstractmethod
    def get(self, pk: int) -> OzonProductEntity | None:
        pass

    @abstractmethod
    def create(
            self, create_data: OzonProductCreateProperties
    ) -> OzonProductEntity:
        pass

    @abstractmethod
    def update(
            self,
            pk: int,
            update_data: OzonProductUpdatableProperties,
    ) -> OzonProductEntity:
        pass

    @abstractmethod
    def create_or_update(
            self, create_data: OzonProductCreateProperties
    ) -> OzonProductEntity:
        pass
