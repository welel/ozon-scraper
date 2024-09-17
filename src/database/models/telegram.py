from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from config import DBConfig
from database.models.base import BaseModel
from database.models.ozon import OzonReview


class TelegramOzonReviewPost(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}tg_ozon_post"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="PK - post ID.",
    )
    review_uuid: Mapped[str] = mapped_column(
        sa.ForeignKey(f"{OzonReview.__tablename__}.uuid"),
        comment="PK - Ozon review media ID",
    )
    admin_comment: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
        default=None,
        comment="Channel admin comment",
    )
    post_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=True,
        default=None,
        comment="Datetime when to make a post.",
    )
    posted_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=True,
        comment="Posted in the channel datetime.",
    )
    is_valid: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=True,
        default=None,
        comment="Flag - is valid to post.",
    )
