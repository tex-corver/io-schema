from datetime import datetime

import pydantic
from io_schema import item as item_schemas


class CartItemsResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    items: dict[str, item_schemas.Item] = pydantic.Field(default_factory=dict)


class CartBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    user_id: str
    items: dict[str, item_schemas.Item] = pydantic.Field(default_factory=dict)


class Cart(CartBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: str
    created_time: datetime
    updated_time: datetime


class CartResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    cart: Cart
