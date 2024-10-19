from enum import Enum

from pydantic import Field, HttpUrl

from scrap.dto.dto import DTO


class OzonMediaType(str, Enum):
    video = "video"
    image = "image"


class BaseOzonReviewMedia(DTO):
    review_uuid: str = Field(
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
    video_duration_sec: int | None = Field(
        None,
        description="Video duration in seconds",
    )
    width: int | None = Field(
        None,
        description="Media width pixels",
    )
    height: int | None = Field(
        None,
        description="Media height pixels",
    )


class OzonReviewMediaCreateProperties(BaseOzonReviewMedia):
    id: str = Field(
        ...,
        description="PK - review media ID - PK (md5 from id from media URL)",
    )


class OzonReviewMediaUpdatableProperties(BaseOzonReviewMedia):
    pass
