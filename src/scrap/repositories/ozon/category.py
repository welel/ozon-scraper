from scrap.database import get_session
from scrap.database.models.ozon import OzonCategory
from scrap.database.models.scraper import ScraperOzonCategoryMeta
from scrap.dto.ozon.category import (
    OzonCategoryCreateProperties,
    OzonCategoryUpdatableProperties,
)
from scrap.entities.ozon import OzonCategoryEntity
from scrap.repositories.ozon.interfaces.category import OzonCategoryInterface
from scrap.repositories.sqlalchemy_repo import SqlalchemyRepository


class OzonCategoriesRepository(
        SqlalchemyRepository[
            int,
            OzonCategoryEntity,
            OzonCategoryCreateProperties,
            OzonCategoryUpdatableProperties,
        ],
        OzonCategoryInterface,
):
    sa_model = OzonCategory
    entity_py_model = OzonCategoryEntity

    def get_list_on_parsing(self) -> list[OzonCategoryEntity]:
        with get_session() as session:
            query = session.query(OzonCategory).join(
                ScraperOzonCategoryMeta,
                OzonCategory.id == ScraperOzonCategoryMeta.category_id,
            ).filter(
                ScraperOzonCategoryMeta.is_parsing_enabled.is_(True),
            ).order_by(
                ScraperOzonCategoryMeta.parsing_priority
            )
            return [self.entity_py_model.model_validate(cat) for cat in query]
