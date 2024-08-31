from abc import ABC, abstractmethod
from typing import Union

from dto.ozon_category import (
    CreateOzonCategoryProperties,
    OzonCategory,
    OzonCategoryUpdatableProperties,
)


class OzonCategoryInterface(ABC):

    @abstractmethod
    def create(self, category: CreateOzonCategoryProperties) -> OzonCategory:
        pass

    @abstractmethod
    def create_or_update(
            self,
            category: Union[
                CreateOzonCategoryProperties, OzonCategoryUpdatableProperties
            ],
    ) -> OzonCategory:
        pass

    @abstractmethod
    def get(self, cat_id: int) -> OzonCategory | None:
        pass

    @abstractmethod
    def get_list_on_parsing(self) -> list[OzonCategory]:
        pass
