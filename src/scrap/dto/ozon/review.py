from pydantic import Field, HttpUrl

from scrap.config import UUID_LEN
from scrap.dto.dto import DTO


class BaseOzonReview(DTO):
    product_sku_id: int = Field(
        ...,
        description="Product Stock Keeping Unit ID",
    )
    rating: int | None = Field(
        None,
        description="Rating given by the reviewer",
    )
    user_name: str | None = Field(
        None,
        max_length=64,
        description="Name of the user who reviewed",
    )
    user_image_url: HttpUrl | None = Field(
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
    like_count: int | None = Field(
        None,
        description="Number of likes on the review",
    )
    dislike_count: int | None = Field(
        None,
        description="Number of dislikes on the review",
    )
    comment_text: str | None = Field(
        None,
        description="Text of the review",
    )
    advantages_text: str | None = Field(
        None,
        description="Text describing the advantages in the review",
    )
    disadvantages_text: str | None = Field(
        None,
        description="Text describing the disadvantages in the review",
    )


class OzonReviewCreateProperties(BaseOzonReview):
    uuid: str = Field(
        ...,
        max_length=UUID_LEN,
        description="Unique identifier for the review",
    )

    @property
    def id(self) -> str:
        return self.uuid


class OzonReviewUpdatableProperties(BaseOzonReview):
    pass
