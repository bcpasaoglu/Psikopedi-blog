"""Request and response models."""

from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _check_image_url(value: str | None) -> str | None:
    if value and not value.startswith(("https://", "http://", "/")):
        raise ValueError("image_url must be an http(s) URL or a site-relative path")
    return value


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(default="Psikopedi", max_length=100)
    date: Date | None = None
    summary: str = Field(default="", max_length=500)
    content: str = ""
    image_url: str = Field(default="", max_length=500)
    slug: str | None = Field(default=None, max_length=200)

    _image = field_validator("image_url")(_check_image_url)


class ArticleUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=100)
    date: Date | None = None
    summary: str | None = Field(default=None, max_length=500)
    content: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
    slug: str | None = Field(default=None, max_length=200)

    _image = field_validator("image_url")(_check_image_url)


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


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
