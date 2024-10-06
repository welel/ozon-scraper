from abc import ABC, abstractmethod

from scrap.dto.ozon.review_media import (
    OzonReviewMedia,
    OzonReviewMediaCreateProperties,
    OzonReviewMediaUpdatableProperties,
)


class OzonReviewMediaInterface(ABC):

    @abstractmethod
    def create(
            self,
            review_media: OzonReviewMediaCreateProperties
    ) -> OzonReviewMedia:
        pass

    @abstractmethod
    def update(
            self,
            id_: str,
            review_media: OzonReviewMediaUpdatableProperties,
    ) -> OzonReviewMedia:
        pass

    @abstractmethod
    def create_or_update(
            self,
            review_media: OzonReviewMediaCreateProperties,
    ) -> OzonReviewMedia:
        pass

    @abstractmethod
    def get(self, id_: str) -> OzonReviewMedia | None:
        pass
