from enum import Enum
from typing import Optional

from pydantic import Field, HttpUrl

from scrap.config import UUID_LEN
from scrap.entities.entity import Entity


class OzonCategoryEntity(Entity):
    id: int
    parent_id: Optional[int] = None
    level: int
    url: HttpUrl
    short_url: HttpUrl
    name: Optional[str] = Field(None, max_length=1024)
    image_url: Optional[HttpUrl] = None


class OzonProductEntity(Entity):
    sku_id: int
    name: Optional[str] = Field(None, max_length=1024)
    price: Optional[int] = None
    original_price: Optional[int] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    url: HttpUrl
    image_url: Optional[HttpUrl] = None
    category_id: Optional[int] = None


class OzonReviewEntity(Entity):
    uuid: str = Field(..., max_length=UUID_LEN)
    product_sku_id: int
    rating: Optional[int] = None
    user_name: Optional[str] = Field(None, max_length=64)
    user_image_url: Optional[HttpUrl] = None
    comment_count: int
    url: HttpUrl
    like_count: Optional[int] = None
    dislike_count: Optional[int] = None
    comment_text: Optional[str] = None
    advantages_text: Optional[str] = None
    disadvantages_text: Optional[str] = None


class OzonMediaType(str, Enum):
    video = "video"
    image = "image"


class OzonReviewMediaEntity(Entity):
    id: str
    review_uuid: str
    type: OzonMediaType
    url: HttpUrl
    extension: str = Field(..., max_length=16)
    video_duration_sec: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
