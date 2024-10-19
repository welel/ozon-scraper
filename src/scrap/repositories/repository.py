import abc
from typing import Any

from scrap.dto.dto import DTO
from scrap.entities.entity import Entity


class ReadRepository[PK: Any, Entity_: Entity](abc.ABC):
    @abc.abstractmethod
    def get(self, pk: PK) -> Entity_ | None:
        pass


class CreateRepository[Entity_: Entity, CreateDTO: DTO](abc.ABC):
    @abc.abstractmethod
    def create(self, create_data: CreateDTO) -> Entity_:
        pass


class UpdateRepository[Entity_: Entity, UpdateDTO: DTO](abc.ABC):
    @abc.abstractmethod
    def update(self, update_data: UpdateDTO) -> Entity_:
        pass


class Repository[PK: Any, Entity_: Entity, CreateDTO: DTO, UpdateDTO: DTO](
    ReadRepository[PK, Entity_],
    CreateRepository[CreateDTO, Entity_],
    UpdateRepository[UpdateDTO, Entity_],
):
    pass
