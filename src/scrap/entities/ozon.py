from enum import Enum

from pydantic import Field, HttpUrl

from scrap.config import UUID_LEN
from scrap.entities.entity import Entity


class OzonCategoryEntity(Entity):
    id: int
    parent_id: int | None = None
    level: int
    url: HttpUrl
    short_url: HttpUrl
    name: str | None = Field(None, max_length=1024)
    image_url: HttpUrl | None = None


class OzonProductEntity(Entity):
    sku_id: int
    name: str | None = Field(None, max_length=1024)
    price: int | None = None
    original_price: int | None = None
    stock: int | None = None
    rating: float | None = None
    review_count: int | None = None
    url: HttpUrl
    image_url: HttpUrl | None = None
    category_id: int | None = None


class OzonReviewEntity(Entity):
    uuid: str = Field(..., max_length=UUID_LEN)
    product_sku_id: int
    rating: int | None = None
    user_name: str | None = Field(None, max_length=64)
    user_image_url: HttpUrl | None = None
    comment_count: int
    url: HttpUrl
    like_count: int | None = None
    dislike_count: int | None = None
    comment_text: str | None = None
    advantages_text: str | None = None
    disadvantages_text: str | None = None


class OzonMediaType(str, Enum):
    video = "video"
    image = "image"


class OzonReviewMediaEntity(Entity):
    id: str
    review_uuid: str
    type: OzonMediaType
    url: HttpUrl
    extension: str = Field(..., max_length=16)
    video_duration_sec: int | None = None
    width: int | None = None
    height: int | None = None
