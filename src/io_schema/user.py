import enum
import re
from datetime import datetime
from typing import Optional, Self

import pydantic

__all__ = [
    "Identity",
    "User",
    "LoggedInUser",
    "LoginResponse",
    "Links",
    "Otp",
    "OtpResponse",
    "Token",
    "TokenResponse",
    "OtpRequiredResponse",
    "ShippingProfile",
    "ShippingProfileResponse",
    "ListShippingProfileResponse",
    "CreateOtp",
    "VerifyOtp",
    "Register",
    "Login",
    "OtpMethod",
    "OtpAction",
    "Action",
    "TracingHeaders",
    "Address",
    "Receiver",
    "ShippingProfileBase",
    "AuthorizationContext",
    "Role",
]


class TracingHeaders(pydantic.BaseModel):
    session_id: Optional[str] | None = None
    device_id: Optional[str] | None = None
    token: Optional[str] | None = None


class Action(enum.StrEnum):
    CREATE_ADMIN_USER = "CREATE_ADMIN_USER"


class OtpMethod(enum.StrEnum):
    EMAIL = "EMAIL"
    SMS = "SMS"


class OtpAction(enum.StrEnum):
    REGISTER = "REGISTER"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    CHANGE_PHONE_NUMBER = "CHANGE_PHONE_NUMBER"
    AUTHENTICATE = "AUTHENTICATE"


class CreateOtp(pydantic.BaseModel):
    """
    CreateOtp.
    """

    model_config = pydantic.ConfigDict(use_enum_values=True)

    receiver: Optional[str] | None = None
    otp_method: OtpMethod | str = OtpMethod.EMAIL
    otp_action: OtpAction | str = OtpAction.REGISTER

    @pydantic.model_validator(mode="after")
    def verify_email_or_phone_number(self) -> Self:
        email = None
        phone_number = None
        if self.receiver is None:
            raise ValueError("receiver must be provided")
        if re.match(r"^[^@]+@[^@]+\.[^@]+$", self.receiver):
            email = self.receiver
        else:
            phone_number = self.receiver
        if email is None and phone_number is None:
            raise ValueError(
                "email or phone_number must be provided",
            )

        if self.otp_method == OtpMethod.EMAIL and email is None:
            raise ValueError(
                "email must be provided if otp_method is EMAIL",
            )

        if self.otp_method == OtpMethod.SMS and phone_number is None:
            raise ValueError(
                "phone_number must be provided if otp_method is SMS",
            )

        return self


class VerifyOtp(pydantic.BaseModel):
    """
    VerifyOtp.
    """

    code: str


class Register(pydantic.BaseModel):
    """
    Register.
    """

    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    re_password: Optional[str] = None

    @pydantic.model_validator(mode="after")
    def verify_password(self) -> Self:
        if self.password != self.re_password:
            raise ValueError("password and re_password must be the same")
        return self


class Login(pydantic.BaseModel):
    """
    Login.
    """

    username: str
    password: str


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
    Recevier.
    """

    name: Optional[str] | None = None
    phone_number: Optional[str] | None = None


class ShippingProfileBase(pydantic.BaseModel):
    name: Optional[str] | None = None
    receiver: Optional[Receiver] | None = None
    address: Address | None = None


import pydantic


class Identity(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    id: str
    created_time: datetime
    updated_time: datetime


class User(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        extra="ignore",
    )

    id: str
    email: Optional[str] | None = None
    phone_number: Optional[str] | None = None
    role: str


class Links(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    verify: str
    resend: str


class Otp(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    id: str
    expiration_time: datetime
    receiver: Optional[str] | None = None
    kind: OtpMethod


class OtpResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    # links: Links
    otp: Otp


class Token(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    value: str


class TokenResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        extra="ignore",
    )

    token: Token


class LoggedInUser(User):
    token: str


class LoginResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    user: LoggedInUser


class OtpRequiredResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True, use_enum_values=True)

    required: bool


class ShippingProfile(ShippingProfileBase):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    id: str
    user_id: str


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


class Role(enum.StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


class AuthorizationContext(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        extra="allow",
    )

    user_id: str
    role: Role = Role.USER
    device_id: str | None = None
