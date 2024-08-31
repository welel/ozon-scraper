from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BaseOzonCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_id: Optional[int] = Field(
        None,
        description="Parent category ID from Ozon",
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
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Category ID from Ozon - PK",
    )


class CreateOzonCategoryProperties(OzonCategory):
    pass


class OzonCategoryUpdatableProperties(BaseOzonCategory):
    pass
