from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from config import UUID_LEN


class BaseOzonReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_sku_id: int = Field(
        ...,
        description="Product Stock Keeping Unit ID",
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
    comment_text: Optional[str] = Field(
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


class OzonReview(BaseOzonReview):
    uuid: str = Field(
        ...,
        max_length=UUID_LEN,
        description="Unique identifier for the review",
    )


class OzonReviewCreateProperties(OzonReview):
    pass


class OzonReviewUpdatableProperties(BaseOzonReview):
    pass
