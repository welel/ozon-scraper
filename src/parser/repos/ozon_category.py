from sqlalchemy.orm import Session

from db import get_session
from db.models.ozon import OzonCategory as DBOzonCategory
from dto.ozon_category import CreateOzonCategoryProperties, OzonCategory
from dto.ozon_category import OzonCategoryUpdatableProperties
from .interfaces.ozon_category import OzonCategoryInterface


class OzonCategoriesRepo(OzonCategoryInterface):

    def _get_from_db(
            self,
            cat_id: int,
            session: Session,
    ) -> DBOzonCategory | None:
        return session.query(DBOzonCategory).filter(
            DBOzonCategory.id == cat_id,
        ).first()

    def _update_by_schema(
            self,
            db_category: DBOzonCategory,
            category: OzonCategoryUpdatableProperties,
    ) -> None:
        for field, value in category.model_dump(mode="json").items():
            setattr(db_category, field, value)

    def create(self, category: CreateOzonCategoryProperties) -> OzonCategory:
        db_category = DBOzonCategory(**category.model_dump(mode="json"))
        with get_session() as session:
            session.add(db_category)
            session.commit()
            return OzonCategory.model_validate(db_category)

    def create_or_update(
            self, category: CreateOzonCategoryProperties,
    ) -> OzonCategory:
        with get_session() as session:
            db_category = self._get_from_db(category.id, session)
            if db_category is None:
                return self.create(category)
            else:
                self._update_by_schema(
                    db_category,
                    OzonCategoryUpdatableProperties.model_validate(
                        category.model_dump(exclude_unset=True),
                    )
                )
                session.commit()
                return OzonCategory.model_validate(db_category)

    def get(self, cat_id: int) -> OzonCategory | None:
        with get_session() as session:
            db_category = self._get_from_db(cat_id, session)
            if db_category is not None:
                return DBOzonCategory.model_validate(db_category)

    def get_list_on_parsing(self) -> list[OzonCategory]:
        with get_session() as session:
            query = session.query(DBOzonCategory).filter(
                DBOzonCategory.is_active_to_parse.is_(True),
            ).order_by(
                DBOzonCategory.parsing_priority
            )
            return [OzonCategory.model_validate(cat) for cat in query]
