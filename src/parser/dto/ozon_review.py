from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from config import UUID_LEN
from .mixins import TimestampsMixin


class BaseOzonReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parsed_by_product_id: int = Field(
        ...,
        description="FK to the product which triggered parsing of this review",
    )
    sku_id: Optional[int] = Field(
        None,
        description="Stock Keeping Unit ID",
    )
    review_uuid: Optional[str] = Field(
        None,
        max_length=UUID_LEN,
        description="Unique identifier for the review",
    )
    review_puuid: Optional[str] = Field(
        None,
        max_length=UUID_LEN,
        description="(product/parent)? unique identifier for the review",
    )
    rating: Optional[int] = Field(
        None,
        description="Rating given by the reviewer",
    )
    user_name: Optional[str] = Field(
        None,
        max_length=64,
        description="Name of the user who reviewed",
    )
    user_image_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the user's profile image",
    )
    comment_count: int = Field(
        ...,
        description="Number of comments on the review",
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the review page",
    )
    like_count: Optional[int] = Field(
        None,
        description="Number of likes on the review",
    )
    dislike_count: Optional[int] = Field(
        None,
        description="Number of dislikes on the review",
    )
    text: Optional[str] = Field(
        None,
        description="Text of the review",
    )
    advantages_text: Optional[str] = Field(
        None,
        description="Text describing the advantages in the review",
    )
    disadvantages_text: Optional[str] = Field(
        None,
        description="Text describing the disadvantages in the review",
    )


class OzonReview(TimestampsMixin, BaseOzonReview):
    id: int = Field(
        ...,
        description="Review ID - PK",
    )


class CreateOzonReviewProperties(BaseOzonReview):
    pass


class OzonReviewUpdatableProperties(BaseOzonReview):
    pass
