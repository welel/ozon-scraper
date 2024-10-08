import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from scrap.config import DBConfig
from scrap.database.models.base import BaseModel
from scrap.database.models.ozon import OzonCategory


class ScraperOzonCategoryMeta(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}scraper_ozon_category_meta"

    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey(f"{OzonCategory.__tablename__}.id"),
        primary_key=True,
        comment="PK - Ozon category ID",
    )
    parsing_priority: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=10_000,
        comment="Parsing priority - less first in a queue",
    )
    is_parsing_enabled: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Wheather to scrape category",
    )
