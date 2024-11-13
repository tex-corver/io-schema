from __future__ import annotations

from datetime import datetime
from typing import Optional

import pydantic

__all__ = [
    "ProductLineAdditionBase",
    "ProductLineAddition",
    "ProductLineAdditionResponse",
    "ProductLineAdditionListResponse",
    "ProductLineOptionBase",
    "ProductLineOption",
    "ProductLineOptionResponse",
    "ProductLineOptionListResponse",
    "ProductLineBase",
    "ProductLine",
    "ProductLineResponse",
    "ProductLineQueryResponse",
    "ProductLineListResponse",
    "Product",
    "ProductResponse",
    "ProductListResponse",
]
from datetime import datetime
from typing import Any, Optional

import pydantic
from io_schema import image as image_schemas, product as product_schemas


class ProductLineOptionBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    kind: Optional[str] = ""
    name: Optional[str] = None
    price: Optional[float] = None
    images: Optional[list[image_schemas.Image]] = pydantic.Field(default_factory=list)
    description: Optional[str] = ""


class ProductLineOption(ProductLineOptionBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: str
    created_time: datetime = pydantic.Field(default_factory=datetime.now)
    updated_time: datetime = pydantic.Field(default_factory=datetime.now)


class ProductLineOptionResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line_option: ProductLineOption


class ProductLineOptionListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line_options: list[ProductLineOption]


class ProductLineAdditionBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    name: Optional[str] = ""
    product_line_id: Optional[str] | None = None
    description: Optional[str] = ""
    images: Optional[list[image_schemas.Image]] = pydantic.Field(default_factory=list)
    delta_amount: Optional[float] = 0.0


class ProductLineAddition(ProductLineAdditionBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: str
    created_time: datetime = pydantic.Field(default_factory=datetime.now)
    updated_time: datetime = pydantic.Field(default_factory=datetime.now)


class ProductLineAdditionResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line_addition: ProductLineAddition


class ProductLineAdditionListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line_additions: list[ProductLineAddition]


class ProductLineBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    name: Optional[str] = ""
    description: Optional[str] = ""
    kind: Optional[str] = "ONE_TIME"
    price: Optional[float] = 0.0
    # labels: Optional[list[str]] = pydantic.Field(default_factory=list)
    images: Optional[list[image_schemas.Image]] = pydantic.Field(default_factory=list)
    options: Optional[dict[str, list[ProductLineOption]]] = pydantic.Field(
        default_factory=dict
    )


class ProductLine(ProductLineBase):
    model_config = pydantic.ConfigDict(from_attributes=True, extra="allow")

    id: str
    created_time: datetime = pydantic.Field(default_factory=datetime.now)
    updated_time: datetime = pydantic.Field(default_factory=datetime.now)


class ProductLineQueryResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_lines: list[ProductLine]


class ProductLineResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line: ProductLine


class ProductLineListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_lines: list[ProductLine]


class ProductMetadata(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product_line: ProductLine
    product_line_options: dict[str, ProductLineOption] = pydantic.Field(
        default_factory=dict
    )


class Product(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    metadata: ProductMetadata

    @property
    def name(self) -> str:
        return self.metadata.product_line.name + "_".join(
            self.metadata.product_line_options.keys()
        )

    @property
    def price(self) -> float:
        return self.metadata.product_line.price + sum(
            [option.price for option in self.metadata.product_line_options.values()]
        )

    @property
    def product_line(self) -> ProductLine:
        return self.metadata.product_line

    @property
    def product_line_options(self) -> dict[str, ProductLineOption]:
        return self.metadata.product_line_options

    @property
    def description(self) -> str:
        return self.metadata.product_line.description + "\n".join(
            [
                option.description
                for option in self.metadata.product_line_options.values()
            ]
        )

    @property
    def images(self) -> list[image_schemas.Image]:
        return self.metadata.product_line.images + [
            option.images for option in self.metadata.product_line_options.values()
        ]

    @classmethod
    def from_product_line_and_options(
        cls,
        product_line: ProductLine,
        options: dict[str, ProductLineOption],
    ) -> ProductBase:
        return cls(
            metadata=ProductMetadata(
                product_line=product_line,
                product_line_options=options,
            )
        )


class ProductResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    product: Product


class ProductListResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    products: list[Product]
