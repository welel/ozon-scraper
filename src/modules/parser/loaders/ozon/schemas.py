from pydantic import BaseModel, Field
from typing import Dict, List


class MediaSize(BaseModel):
    width: int
    height: int


class Media(BaseModel):
    type: str
    rating: int
    url: str
    video_duration: str = Field(..., alias="videoDuration")
    size: MediaSize
    uuid: str
    review_uuid: str = Field(..., alias="reviewUuid")


class Author(BaseModel):
    first_name: str = Field(..., alias="firstName")
    fio: str
    avatar_url: str = Field(..., alias="avatarUrl")


class Usefulness(BaseModel):
    useful: int
    unuseful: int


class Content(BaseModel):
    score: int
    comment: str
    positive: str
    negative: str


class Comments(BaseModel):
    total_count: int = Field(..., alias="totalCount")


class Sharing(BaseModel):
    url: str


class Review(BaseModel):
    author: Author
    usefulness: Usefulness
    is_anonymous: bool = Field(..., alias="isAnonymous")
    content: Content
    comments: Comments
    sharing: Sharing
    uuid: str


class ReviewsDataState(BaseModel):
    media: List[Media]
    reviews: Dict[str, Review]

    class Config:
        populate_by_name = True
