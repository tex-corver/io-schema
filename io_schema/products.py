from datetime import datetime
from typing import Optional

import pydantic

__all__ = [
    "ProductBase",
    "ProductSchema",
    "ProductResponse",
    "ProductListResponse",
]


class ProductBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None


class ProductSchema(ProductBase):
    model_config = pydantic.ConfigDict(from_attributes=True, extra="allow")

    id: str
    created_time: datetime = pydantic.Field(default_factory=datetime.now)
    updated_time: datetime = pydantic.Field(default_factory=datetime.now)


class ProductResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product: ProductSchema


class ProductListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    products: list[ProductSchema]
