__all__ = [
    "ItemMetadataBase",
    "ItemBase",
    "Item",
    "ItemResponse",
]
from datetime import datetime
from typing import Optional

import pydantic

from io_schema import products


class ItemMetadata(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product: products.Product | None = None


class ItemBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    metadata: Optional[ItemMetadata] = None
    quantity: Optional[int] = 1


class Item(ItemBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: str
    created_time: datetime
    updated_time: datetime


class ItemResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    item: Item
