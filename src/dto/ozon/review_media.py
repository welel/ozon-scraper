from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class OzonMediaType(str, Enum):
    video = "video"
    image = "image"


class BaseOzonReviewMedia(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_uuid: int = Field(
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
    extension: str = Field(
        ...,
        max_length=16,
        description="File extension of the media (without dot).",
    )
    video_duration_sec: Optional[int] = Field(
        None,
        description="Video duration in seconds",
    )
    width: Optional[int] = Field(
        None,
        description="Media width pixels",
    )
    height: Optional[int] = Field(
        None,
        description="Media height pixels",
    )


class OzonReviewMedia(BaseOzonReviewMedia):
    id: str = Field(
        ...,
        description="PK - review media ID - PK (md5 from id from media URL)",
    )


class OzonReviewMediaCreateProperties(OzonReviewMedia):
    pass


class OzonReviewMediaUpdatableProperties(BaseOzonReviewMedia):
    pass
