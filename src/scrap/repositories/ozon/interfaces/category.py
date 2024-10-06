from abc import ABC, abstractmethod

from scrap.dto.ozon.category import (
    OzonCategoryCreateProperties,
    OzonCategoryUpdatableProperties,
)
from scrap.entities.ozon import OzonCategoryEntity


class OzonCategoryInterface(ABC):

    @abstractmethod
    def create(
            self, create_data: OzonCategoryCreateProperties
    ) -> OzonCategoryEntity:
        pass

    @abstractmethod
    def update(
            self,
            pk: int,
            update_data: OzonCategoryUpdatableProperties,
    ) -> OzonCategoryEntity:
        pass

    @abstractmethod
    def create_or_update(
            self,
            create_data: OzonCategoryCreateProperties,
    ) -> OzonCategoryEntity:
        pass

    @abstractmethod
    def get(self, pk: int) -> OzonCategoryEntity | None:
        pass

    @abstractmethod
    def get_list_on_parsing(self) -> list[OzonCategoryEntity]:
        pass
