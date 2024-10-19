from pydantic import Field, HttpUrl

from scrap.dto.dto import DTO


class BaseOzonCategory(DTO):
    parent_id: int | None = Field(
        None,
        description="Parent category ID from Ozon",
    )
    level: int = Field(
        ...,
        description="Category level in the category tree",
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the category page",
    )
    short_url: HttpUrl = Field(
        ...,
        description="Short URL to the category page",
    )
    name: str | None = Field(
        None,
        max_length=1024,
        description="Category name",
    )
    image_url: HttpUrl | None = Field(
        None,
        description="URL to the category image",
    )


class OzonCategoryCreateProperties(BaseOzonCategory):
    id: int = Field(
        ...,
        description="Ozon category ID",
    )


class OzonCategoryUpdatableProperties(BaseOzonCategory):
    pass
