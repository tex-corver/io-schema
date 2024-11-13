from datetime import datetime
from typing import Optional

import pydantic

__all__ = [
    "ImageBase",
    "Image",
    "ImageResponse",
    "ImageListResponse",
]


class ImageBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    path: Optional[str]
    order: int = 0


class Image(ImageBase):
    model_config = pydantic.ConfigDict(from_attributes=True, extra="allow")

    id: str
    created_time: datetime = pydantic.Field(default_factory=datetime.now)
    updated_time: datetime = pydantic.Field(default_factory=datetime.now)


class ImageResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    image: Image


class ImageListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    images: list[Image]
