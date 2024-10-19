from pydantic import Field, HttpUrl

from scrap.dto.dto import DTO


class BaseOzonProduct(DTO):
    name: str | None = Field(
        None,
        max_length=1024,
        description="Product name",
    )
    price: int | None = Field(
        None,
        description="Current price of the product in RUB",
    )
    original_price: int | None = Field(
        None,
        description="Original price of the product before discount in RUB",
    )
    stock: int | None = Field(
        None,
        description="Stock availability",
    )
    rating: float | None = Field(
        None,
        description="Average rating of the product",
    )
    review_count: int | None = Field(
        None,
        description="Number of reviews for the product",
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the product page",
    )
    image_url: HttpUrl | None = Field(
        None,
        description="URL to the product image",
    )
    category_id: int | None = Field(
        None,
        description="Category ID which triggered parsing of this product",
    )


class OzonProductCreateProperties(BaseOzonProduct):
    sku_id: int = Field(
        ...,
        description="Stock Keeping Unit ID",
    )

    @property
    def id(self) -> int:
        return self.sku_id


class OzonProductUpdatableProperties(BaseOzonProduct):
    pass
