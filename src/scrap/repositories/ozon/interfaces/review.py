from abc import ABC, abstractmethod

from scrap.dto.ozon.review import (
    OzonReviewCreateProperties,
    OzonReviewUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewEntity


class OzonReviewInterface(ABC):

    @abstractmethod
    def get(self, pk: str) -> OzonReviewEntity | None:
        pass

    @abstractmethod
    def create(
            self, create_data: OzonReviewCreateProperties
    ) -> OzonReviewEntity:
        pass

    @abstractmethod
    def update(
            self,
            pk: str,
            update_data: OzonReviewUpdatableProperties,
    ) -> OzonReviewEntity:
        pass

    @abstractmethod
    def create_or_update(
            self, create_data: OzonReviewCreateProperties
    ) -> OzonReviewEntity:
        pass
