from typing import Any, Type

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from scrap.database import get_session
from scrap.dto.dto import DTO
from scrap.entities.entity import Entity
from scrap.repositories.exc import ObjectExists, ObjectNotExists
from scrap.repositories.repository import Repository


class SqlalchemyRepository[
    PK: Any, Entity_: Entity, CreateDTO: DTO, UpdateDTO: DTO
](
    Repository[PK, CreateDTO, UpdateDTO, Entity_]
):
    """Base repository managed by sqlalchemy.

    Attributes:
        sa_model: Sqlalchemy model class.
        entity_py_model: Entity (pydantic) class.

    """
    sa_model: Type[DeclarativeMeta]
    entity_py_model: Type[Entity_]

    def _get(
            self, pk: PK, session: Session
    ) -> DeclarativeMeta | None:
        return session.get(self.sa_model, pk)

    def _update_fields_by_schema(
            self, db_object: DeclarativeMeta, schema: BaseModel
    ) -> None:
        update_properties = schema.model_dump(mode="json", exclude_unset=True)
        for field, value in update_properties.items():
            setattr(db_object, field, value)

    def _update(
            self,
            pk: Any,
            schema: BaseModel,
            session: Session,
    ) -> BaseModel:
        db_object = self._get(pk, session)
        if db_object is None:
            raise ObjectNotExists(missin_pk=pk)
        self._update_fields_by_schema(db_object, schema)
        session.commit()
        return self.entity_py_model.model_validate(db_object)

    def _create_from_schema(
            self, schema: BaseModel, session: Session
    ) -> DeclarativeMeta:
        db_object = self.sa_model(**schema.model_dump(mode="json"))
        session.add(db_object)
        try:
            session.commit()
        except IntegrityError:
            raise ObjectExists
        return db_object

    def _create(self, schema: BaseModel, session: Session) -> BaseModel:
        db_object = self._create_from_schema(schema, session)
        return self.entity_py_model.model_validate(db_object)

    def _create_or_update(
            self,
            pk: PK,
            schema: BaseModel,
            session: Session,
    ) -> BaseModel:
        db_object = self._get(pk, session)
        if db_object is None:
            return self._create(schema, session)
        return self._update(pk, schema, session)

    def get(self, pk: PK) -> Entity_ | None:
        with get_session() as session:
            return self._get(pk, session)

    def create(self, create_data: CreateDTO) -> Entity_:
        with get_session() as session:
            self._create(create_data, session)

    def update(self, pk: PK, update_data: UpdateDTO) -> Entity_:
        with get_session() as session:
            return self._update(pk, update_data, session)

    def create_or_update(self, create_data: CreateDTO) -> Entity_:
        with get_session() as session:
            return self._create_or_update(
                create_data.id, create_data, session
            )
