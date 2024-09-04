from database import get_session
from database.models.ozon import OzonCategory as OzonCategoryModel
from dto.ozon.category import (
    OzonCategory,
    OzonCategoryCreateProperties,
    OzonCategoryUpdatableProperties,
)
from ..sqlalchemy_base import SqlalchemyBaseRepo
from .interfaces.category import OzonCategoryInterface


class OzonCategoriesRepo(SqlalchemyBaseRepo, OzonCategoryInterface):
    sa_model = OzonCategoryModel
    py_model = OzonCategory

    def create(self, category: OzonCategoryCreateProperties) -> OzonCategory:
        with get_session() as session:
            self._create(category, session)

    def update(
            self,
            id_: int,
            category: OzonCategoryUpdatableProperties,
    ) -> OzonCategory:
        with get_session() as session:
            return self._update(id_, category, session)

    def create_or_update(
            self,
            category: OzonCategoryCreateProperties,
    ) -> OzonCategory:
        with get_session() as session:
            return self._create_or_update(category.id, category, session)

    def get(self, id_: int) -> OzonCategory | None:
        with get_session() as session:
            return self._get(id_, session)

    def get_list_on_parsing(self) -> list[OzonCategory]:
        # with get_session() as session:
        #     query = session.query(OzonCategoryModel).filter(
        #         OzonCategoryModel.is_active_to_parse.is_(True),
        #     ).order_by(
        #         OzonCategoryModel.parsing_priority
        #     )
        #     return [OzonCategory.model_validate(cat) for cat in query]
        return []
