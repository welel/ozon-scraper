import enum
from datetime import datetime
from datetime import time as datetime_time

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column

from config import URL_MAX_LEN, DBConfig
from database.models.base import BaseModel
from database.models.mixins import TimestampsMixin


class PostTemplate(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_template"
    DEFAULT_NAME = "default"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Template ID",
    )
    name: Mapped[str] = mapped_column(
        sa.String(256),
        nullable=False,
        comment="Name of the template",
    )
    template_content: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        comment="Content of the template",
    )
    required_params: Mapped[list[str]] = mapped_column(
        ARRAY(sa.String(32)),
        nullable=False,
        default=list,
        comment="Required params to render template",
    )


class PostType(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_type"
    DEFAULT_NAME = "default"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Post Type ID",
    )
    name: Mapped[str] = mapped_column(
        sa.String(128),
        nullable=False,
        unique=True,
        comment="Post type name",
    )
    post_template_id: Mapped[int | None] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{PostTemplate.__tablename__}.id"),
        nullable=True,
        comment="Foreign key to PostTemplate (use default for None)",
    )


class Post(TimestampsMixin, BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Post ID",
    )
    title: Mapped[str] = mapped_column(
        sa.String(256),
        default="",
        comment="Title of the post",
    )
    content: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Content generated from template",
    )
    template_params: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict,
        comment="Parameters used for rendering template",
    )
    post_type_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{PostType.__tablename__}.id"),
        nullable=True,
        comment="Foreign key to PostType (use default for None).",
    )
    data: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict,
        comment="Additional data",
    )


class PostMediaType(enum.Enum):
    image = "image"
    video = "video"


class PostMedia(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_media"
    Type = PostMediaType

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Post Media ID",
    )
    type: Mapped[PostMediaType] = mapped_column(
        sa.Enum(PostMediaType, name="post_media_type"),
        nullable=False,
        comment="Type of the media",
    )
    caption: Mapped[str] = mapped_column(
        sa.String(256),
        nullable=True,
        default=None,
        comment="Caption of the media",
    )
    url: Mapped[str] = mapped_column(
        sa.String(URL_MAX_LEN),
        nullable=False,
        comment="URL of the media",
    )
    post_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{Post.__tablename__}.id"),
        nullable=False,
        comment="Foreign key to Post",
    )


class PostPool(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_pool"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key for the post pool",
    )
    name: Mapped[str] = mapped_column(
        sa.String(256),
        nullable=False,
        comment="Name of the post pool",
    )


class PostPoolPost(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_pool_post"

    post_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{Post.__tablename__}.id"),
        primary_key=True,
        comment="Foreign key to Post",
    )
    pool_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{PostPool.__tablename__}.id"),
        primary_key=True,
        comment="Foreign key to PostPool",
    )
    order: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=True,
        comment="Value for ordering posts in the pool",
    )
    added_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=sa.func.now(),
        comment="Datetime of addition to the pool",
    )
    posted_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        nullable=True,
        comment="Datetime of posting",
    )


class Channel(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}channel"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Channel ID",
    )
    name: Mapped[str] = mapped_column(
        sa.String(128),
        nullable=False,
        comment="Name of the channel",
    )
    description: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Description of the channel",
    )
    chat_id: Mapped[str] = mapped_column(
        sa.String(32),
        nullable=False,
        comment="Telegram chat id for bot posting",
    )


class Weekday(str, enum.Enum):
    Mon = ("Mon", 0)
    Tue = ("Tue", 1)
    Wed = ("Wed", 2)
    Thu = ("Thu", 3)
    Fri = ("Fri", 4)
    Sat = ("Sat", 5)
    Sun = ("Sun", 6)

    def __new__(cls, value: str, index_: int):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.index = index_
        return obj


class PostSchedulerTrigger(BaseModel):
    __tablename__ = f"{DBConfig.table_prefix}post_scheduler_trigger"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Trigger ID",
    )
    name: Mapped[str] = mapped_column(
        sa.String(128),
        nullable=False,
        comment="Name of the trigger",
    )
    channel_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{Channel.__tablename__}.id"),
        nullable=False,
        comment="Foreign key to Channel",
    )
    post_type_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{PostType.__tablename__}.id"),
        nullable=False,
        comment="Foreign key to PostType",
    )
    post_pool_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey(f"{PostPool.__tablename__}.id"),
        nullable=False,
        comment="Foreign key to PostPool",
    )
    time: Mapped[datetime_time] = mapped_column(
        sa.Time,
        nullable=False,
        comment="Time of day to run the trigger",
    )
    weekdays: Mapped[list[Weekday]] = mapped_column(
        ARRAY(sa.Enum(Weekday, name="weekday_enum")),
        nullable=False,
        comment="Weekdays to run the job (array of weekdays)",
    )
