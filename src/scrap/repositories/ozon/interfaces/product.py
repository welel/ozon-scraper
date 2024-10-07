import abc

from scrap.dto.ozon.product import (
    OzonProductCreateProperties,
    OzonProductUpdatableProperties,
)
from scrap.entities.ozon import OzonProductEntity
from scrap.repositories.repository import Repository


class OzonProductInterface(
    Repository[
        int,
        OzonProductEntity,
        OzonProductCreateProperties,
        OzonProductUpdatableProperties,
    ],
):

    @abc.abstractmethod
    def create_or_update(
            self, create_data: OzonProductCreateProperties
    ) -> tuple[OzonProductEntity, bool]:
        pass
