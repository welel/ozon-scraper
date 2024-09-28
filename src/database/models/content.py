import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from config import DBConfig
from database.models.base import BaseModel
from database.models.ozon import OzonReviewMedia
from database.models.telegram import Post


class PostOzonReviewMedia(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_ozon_review_media"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="PK of the relation"
    )
    post_id: Mapped[int] = mapped_column(
        sa.ForeignKey(f"{Post.__tablename__}.id"),
        comment="FK on post ID",
        nullable=True,
    )
    review_media_id: Mapped[str] = mapped_column(
        sa.ForeignKey(f"{OzonReviewMedia.__tablename__}.id"),
        comment="FK on review media ID",
    )
    is_decliend: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        comment="Review media decliend for post on the moderation",
    )
