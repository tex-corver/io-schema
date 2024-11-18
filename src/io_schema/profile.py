from datetime import date
from typing import Optional

import pydantic

__all__ = [
    "Address",
    "Profile",
    "ProfileBase",
    "ProfileResponse",
    "Receiver",
    "ShippingProfile",
    "ShippingProfileBase",
    "ShippingProfileResponse",
]


class Address(pydantic.BaseModel):
    """
    Address.
    """

    city: Optional[str] | None = None
    district: Optional[str] | None = None
    ward: Optional[str] | None = None
    street: Optional[str] | None = None
    zip_code: Optional[str] = None


class Receiver(pydantic.BaseModel):
    """
    Receiver.
    """

    name: Optional[str] | None = None
    phone_number: Optional[str] | None = None


class ProfileBase(pydantic.BaseModel):
    gender: Optional[str] | None = None
    date_of_birth: Optional[date] | None = None
    user_id: str
    receiver: Receiver
    address: Address


class ShippingProfileBase(pydantic.BaseModel):
    name: Optional[str] | None = None
    receiver: Optional[Receiver] | None = None
    address: Address | None = None


class Profile(ProfileBase):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )
    id: str


class ProfileResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    profile: Profile


class ShippingProfile(ShippingProfileBase):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    id: str
    user_id: str
    is_default: bool


class ShippingProfileResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    shipping_profile: ShippingProfile


class ListShippingProfileResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    shipping_profiles: list[ShippingProfile]
