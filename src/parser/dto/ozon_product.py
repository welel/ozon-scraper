from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .mixins import TimestampsMixin


class BaseOzonProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sku_id: int = Field(
        ...,
        description="Stock Keeping Unit ID",
    )
    name: Optional[str] = Field(
        None,
        max_length=1024,
        description="Product name",
    )
    price: Optional[int] = Field(
        None,
        description="Current price of the product in RUB",
    )
    original_price: Optional[int] = Field(
        None,
        description="Original price of the product before discount in RUB",
    )
    stock: Optional[int] = Field(
        None,
        description="Stock availability",
    )
    rating: Optional[float] = Field(
        None,
        description="Average rating of the product",
    )
    review_count: Optional[int] = Field(
        None,
        description="Number of reviews for the product",
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the product page",
    )
    image_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the product image",
    )
    category_id: Optional[int] = Field(
        None,
        description="Category ID which triggered parsing of this product",
    )


class OzonProduct(TimestampsMixin, BaseOzonProduct):
    id: int = Field(
        ...,
        description="Product ID - PK",
    )


class CreateOzonProductProperties(BaseOzonProduct):
    pass


class OzonProductUpdatableProperties(BaseOzonProduct):
    pass
