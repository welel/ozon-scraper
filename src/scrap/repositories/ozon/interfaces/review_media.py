import abc

from scrap.dto.ozon.review_media import (
    OzonReviewMediaCreateProperties,
    OzonReviewMediaUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewMediaEntity
from scrap.repositories.repository import Repository


class OzonReviewMediaInterface(
    Repository[
        str,
        OzonReviewMediaEntity,
        OzonReviewMediaCreateProperties,
        OzonReviewMediaUpdatableProperties,
    ],
):
    @abc.abstractmethod
    def create_or_update(
        self, review_media: OzonReviewMediaCreateProperties
    ) -> tuple[OzonReviewMediaEntity, bool]:
        pass
