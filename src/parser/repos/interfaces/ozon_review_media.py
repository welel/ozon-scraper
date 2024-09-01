from abc import ABC, abstractmethod

from dto.ozon_review_media import (
    CreateOzonReviewMediaProperties,
    OzonReviewMedia,
)


class OzonReviewMediaInterface(ABC):

    @abstractmethod
    def create(
            self,
            review_media: CreateOzonReviewMediaProperties,
    ) -> OzonReviewMedia:
        pass

    @abstractmethod
    def create_or_update(
            self,
            review_media: CreateOzonReviewMediaProperties,
    ) -> OzonReviewMedia:
        pass
