from abc import ABC, abstractmethod

from dto.ozon_review import (
    CreateOzonReviewProperties,
    OzonReview,
)


class OzonReviewInterface(ABC):

    @abstractmethod
    def create(self, review: CreateOzonReviewProperties) -> OzonReview:
        pass

    @abstractmethod
    def create_or_update(
            self,
            review: CreateOzonReviewProperties,
    ) -> OzonReview:
        pass
