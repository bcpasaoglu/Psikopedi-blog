"""Request and response models."""

import re
from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from .categories import CATEGORY_SLUGS, DEFAULT_CATEGORY


def _check_image_url(value: str | None) -> str | None:
    if value and not value.startswith(("https://", "http://", "/")):
        raise ValueError("image_url must be an http(s) URL or a site-relative path")
    return value


def _check_category(value: str | None) -> str | None:
    if value is not None and value not in CATEGORY_SLUGS:
        raise ValueError(f"unknown category, expected one of: {', '.join(sorted(CATEGORY_SLUGS))}")
    return value


_TAG_RE = re.compile(r"<[^>]+>")


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(default="Psikopedi", max_length=100)
    date: Date | None = None
    summary: str = Field(default="", max_length=500)
    content: str = ""
    image_url: str = Field(default="", max_length=500)
    slug: str | None = Field(default=None, max_length=200)
    category: str = DEFAULT_CATEGORY

    _image = field_validator("image_url")(_check_image_url)
    _category = field_validator("category")(_check_category)


class ArticleUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=100)
    date: Date | None = None
    summary: str | None = Field(default=None, max_length=500)
    content: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
    slug: str | None = Field(default=None, max_length=200)
    category: str | None = None

    _image = field_validator("image_url")(_check_image_url)
    _category = field_validator("category")(_check_category)


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    author: str
    date: Date
    summary: str
    content: str
    image_url: str
    category: str

    @computed_field
    @property
    def reading_minutes(self) -> int:
        """Estimated reading time at ~200 words per minute, at least one minute."""
        words = len(_TAG_RE.sub(" ", self.content).split())
        return max(1, round(words / 200))


class CategoryOut(BaseModel):
    slug: str
    name: str
    description: str
    count: int


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
