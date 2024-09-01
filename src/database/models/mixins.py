from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class TimestampsMixin:
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=sa.func.now(),
        comment="Timestamp of record creation",
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=sa.func.now(),
        onupdate=sa.func.now(),
        comment="Timestamp of last record update",
    )
