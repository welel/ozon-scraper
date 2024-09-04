from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BaseOzonCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_id: Optional[int] = Field(
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
    name: Optional[str] = Field(
        None,
        max_length=1024,
        description="Category name",
    )
    image_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the category image",
    )


class OzonCategory(BaseOzonCategory):
    id: int = Field(
        ...,
        description="Category ID from Ozon - PK",
    )


class OzonCategoryCreateProperties(OzonCategory):
    pass


class OzonCategoryUpdatableProperties(BaseOzonCategory):
    pass
