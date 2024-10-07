import abc

from scrap.dto.ozon.category import (
    OzonCategoryCreateProperties,
    OzonCategoryUpdatableProperties,
)
from scrap.entities.ozon import OzonCategoryEntity
from scrap.repositories.repository import Repository


class OzonCategoryInterface(
    Repository[
        int,
        OzonCategoryEntity,
        OzonCategoryCreateProperties,
        OzonCategoryUpdatableProperties,
    ],
):

    @abc.abstractmethod
    def create_or_update(
            self,
            create_data: OzonCategoryCreateProperties,
    ) -> OzonCategoryEntity:
        pass

    @abc.abstractmethod
    def get_list_on_parsing(self) -> list[OzonCategoryEntity]:
        pass
