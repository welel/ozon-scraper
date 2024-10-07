import abc

from scrap.dto.ozon.review import (
    OzonReviewCreateProperties,
    OzonReviewUpdatableProperties,
)
from scrap.entities.ozon import OzonReviewEntity
from scrap.repositories.repository import Repository


class OzonReviewInterface(
    Repository[
        str,
        OzonReviewEntity,
        OzonReviewCreateProperties,
        OzonReviewUpdatableProperties,
    ],
):

    @abc.abstractmethod
    def create_or_update(
            self, create_data: OzonReviewCreateProperties
    ) -> tuple[OzonReviewEntity, bool]:
        pass
