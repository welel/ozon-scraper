from datetime import datetime

from pydantic import Field


class TimestampsMixin:
    created_at: datetime = Field(
        ...,
        description="Timestamp of record creation",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp of last record update",
    )
