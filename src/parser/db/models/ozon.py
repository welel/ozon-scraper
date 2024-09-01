import enum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from config import DBConfig, URL_MAX_LEN, UUID_LEN
from db.models.base import BaseModel
from db.models.mixins import TimestampsMixin


class OzonCategory(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}ozon_category"
    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Category ID from Ozon - PK",
    )
    parent_id: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Parent category ID from Ozon",
    )
    url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="URL to the category page",
    )
    short_url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="Short URL to the category page",
    )
    name: Mapped[str | None] = mapped_column(
        sa.String(1024),
        nullable=True,
        comment="Category name",
    )
    image_url: Mapped[str | None] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=True,
        comment="URL to the category image",
    )
    parsing_priority: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=10_000,
        comment="Category parsing priority (0 is parsed first)",
    )
    is_active_to_parse: Mapped[int] = mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Wheather to parse the category while parsing",
    )


class OzonProduct(TimestampsMixin, BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}ozon_product"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Product ID - PK",
    )
    sku_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        nullable=False,
        unique=True,
        comment="Stock Keeping Unit ID",
    )
    name: Mapped[str | None] = mapped_column(
        sa.String(1024),
        nullable=True,
        comment="Product name",
    )
    price: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Current price of the product in RUB",
    )
    original_price: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Original price of the product before discount in RUB",
    )
    stock: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Stock availability",
    )
    rating: Mapped[float | None] = mapped_column(
        sa.Float,
        nullable=True,
        comment="Average rating of the product",
    )
    review_count: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Number of reviews for the product",
    )
    url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="URL to the product page",
    )
    image_url: Mapped[str | None] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=True,
        comment="URL to the product image",
    )
    category_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{OzonCategory.__tablename__}.id"),
        nullable=True,
        comment="FK to the category which triggered parsing of this product",
    )


class OzonReview(TimestampsMixin, BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}ozon_review"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Review ID - PK",
    )
    parsed_by_product_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{OzonProduct.__tablename__}.id"),
        nullable=False,
        comment="FK to the product which triggered parsing of this review",
    )
    sku_id: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        nullable=True,
        comment="Stock Keeping Unit ID",
    )
    review_uuid: Mapped[str | None] = mapped_column(
        sa.String(UUID_LEN),
        nullable=False,
        unique=True,
        comment="Unique identifier for the review",
    )
    review_puuid: Mapped[str | None] = mapped_column(
        sa.String(UUID_LEN),
        nullable=True,
        comment="(product/parent)? unique identifier for the review",
    )
    rating: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Rating given by the reviewer",
    )
    user_name: Mapped[str | None] = mapped_column(
        sa.String(64),
        nullable=True,
        comment="Name of the user who reviewed",
    )
    user_image_url: Mapped[str | None] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=True,
        comment="URL to the user's profile image",
    )
    comment_count: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        comment="Number of comments on the review",
    )
    url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="URL to the review page",
    )
    like_count: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Number of likes on the review",
    )
    dislike_count: Mapped[int | None] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Number of dislikes on the review",
    )
    text: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Text of the review",
    )
    advantages_text: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Text describing the advantages in the review",
    )
    disadvantages_text: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Text describing the disadvantages in the review",
    )


class OzonMediaType(str, enum.Enum):
    video = "video"
    image = "image"


class OzonReviewMedia(TimestampsMixin, BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}ozon_review_media"
    Type = OzonMediaType

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Product Media ID - PK",
    )
    review_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{OzonReview.__tablename__}.id"),
        nullable=False,
        comment="Foreign Key to OzonReview",
    )
    type: Mapped[OzonMediaType] = mapped_column(
        sa.Enum(OzonMediaType, name="ozon_media_type"),
        nullable=False,
        comment="Type of media (video or image)",
    )
    url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="URL to the media resource",
    )
    template_url: Mapped[str | None] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=True,
        comment="Template URL for the media resource",
    )
    extension: Mapped[str] = mapped_column(
        sa.String(16),
        nullable=False,
        comment="File extension of the media (without dot).",
    )
