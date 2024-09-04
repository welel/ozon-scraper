from abc import ABC, abstractmethod

from dto.ozon.review import (
    OzonReview,
    OzonReviewCreateProperties,
    OzonReviewUpdatableProperties,
)


class OzonReviewInterface(ABC):

    @abstractmethod
    def create(self, review: OzonReviewCreateProperties) -> OzonReview:
        pass

    @abstractmethod
    def update(
            self,
            uuid: str,
            review: OzonReviewUpdatableProperties,
    ) -> OzonReview:
        pass

    @abstractmethod
    def create_or_update(
            self,
            review: OzonReviewCreateProperties,
    ) -> OzonReview:
        pass

    @abstractmethod
    def get(self, uuid: str) -> OzonReview | None:
        pass
