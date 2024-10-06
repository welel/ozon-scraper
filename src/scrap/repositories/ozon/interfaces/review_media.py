from abc import ABC, abstractmethod

from scrap.dto.ozon.review_media import (
    OzonReviewMediaCreateProperties,
    OzonReviewMediaUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewMediaEntity


class OzonReviewMediaInterface(ABC):

    @abstractmethod
    def get(self, pk: str) -> OzonReviewMediaEntity | None:
        pass

    @abstractmethod
    def create(
            self, create_data: OzonReviewMediaCreateProperties
    ) -> OzonReviewMediaEntity:
        pass

    @abstractmethod
    def update(
            self,
            pk: str,
            update_data: OzonReviewMediaUpdatableProperties,
    ) -> OzonReviewMediaEntity:
        pass

    @abstractmethod
    def create_or_update(
            self, review_media: OzonReviewMediaCreateProperties
    ) -> OzonReviewMediaEntity:
        pass
