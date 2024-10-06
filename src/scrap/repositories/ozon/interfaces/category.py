from abc import ABC, abstractmethod

from scrap.dto.ozon.category import (
    OzonCategory,
    OzonCategoryCreateProperties,
    OzonCategoryUpdatableProperties,
)


class OzonCategoryInterface(ABC):

    @abstractmethod
    def create(self, category: OzonCategoryCreateProperties) -> OzonCategory:
        pass

    @abstractmethod
    def update(
            self,
            id_: int,
            category: OzonCategoryUpdatableProperties,
    ) -> OzonCategory:
        pass

    @abstractmethod
    def create_or_update(
            self,
            category: OzonCategoryCreateProperties,
    ) -> OzonCategory:
        pass

    @abstractmethod
    def get(self, id_: int) -> OzonCategory | None:
        pass

    @abstractmethod
    def get_list_on_parsing(self) -> list[OzonCategory]:
        pass
