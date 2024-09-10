import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from config import DBConfig
from database.models.base import BaseModel
from database.models.ozon import OzonReviewMedia


class OzonReviewMediaLabel(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}label_ozon_review_media"

    review_media_id: Mapped[int] = mapped_column(
        sa.ForeignKey(f"{OzonReviewMedia.__tablename__}.id"),
        primary_key=True,
        comment="PK - Ozon review media ID",
    )
    label: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Ozon review media label",
    )
