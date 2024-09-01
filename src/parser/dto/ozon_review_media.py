from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .mixins import TimestampsMixin


class OzonMediaType(str, Enum):
    video = "video"
    image = "image"


class BaseOzonReviewMedia(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int = Field(
        ...,
        description="Foreign Key to OzonReview",
    )
    type: OzonMediaType = Field(
        ...,
        description="Type of media (video or image)",
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the media resource",
    )
    template_url: Optional[HttpUrl] = Field(
        None,
        description="Template URL for the media resource",
    )
    extension: str = Field(
        ...,
        max_length=16,
        description="File extension of the media (without dot).",
    )


class OzonReviewMedia(TimestampsMixin, BaseOzonReviewMedia):
    id: int = Field(
        ...,
        description="Product Media ID - PK",
    )


class CreateOzonReviewMediaProperties(BaseOzonReviewMedia):
    pass


class OzonReviewMediaUpdatableProperties(BaseOzonReviewMedia):
    pass
