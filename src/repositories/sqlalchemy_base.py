from typing import Any, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from pydantic import BaseModel

from .exc import ObjectExists, ObjectNotExists


class SqlalchemyBaseRepo:
    """Base repository managed by sqlalchemy.

    Attributes:
        sa_model: Sqlalchemy model class.
        py_model: Pydantic (dto) class (with model config
            from_attributes set in true).

    """
    sa_model: Type[DeclarativeMeta]
    py_model: Type[BaseModel]

    def _get(
            self, pk: Any, session: Session
    ) -> DeclarativeMeta | None:
        return session.get(self.sa_model, pk)

    def _update_fields_by_schema(
            self, db_object: DeclarativeMeta, schema: BaseModel
    ) -> None:
        for field, value in schema.model_dump(mode="json").items():
            setattr(db_object, field, value)

    def _update(
            self,
            pk: Any,
            schema: BaseModel,
            session: Session,
    ) -> BaseModel:
        db_object = self._get(pk, session)
        if db_object is None:
            raise ObjectNotExists
        self._update_fields_by_schema(db_object, schema)
        session.commit()
        return self.py_model.model_validate(db_object)

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
        return self.py_model.model_validate(db_object)

    def _create_or_update(
            self,
            pk: Any,
            schema: BaseModel,
            session: Session,
    ) -> BaseModel:
        db_object = self._get(pk, session)
        if db_object is None:
            return self._create(schema, session)
        return self._update(pk, schema, session)
