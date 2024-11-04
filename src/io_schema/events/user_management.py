import core
import pydantic

from io_schema import users as user_schemas


class GeneratedOtpEvent(core.Event):
    """
    GeneratedOtpEvent.
    """

    model_config = pydantic.ConfigDict(use_enum_values=True, from_attributes=True)

    otp_id: str
    code: str
    receiver: str
    kind: user_schemas.OtpMethod


class GeneratedEmailOtpEvent(GeneratedOtpEvent):
    """
    GeneratedEmailOtpEvent.
    """

    kind: user_schemas.OtpMethod = user_schemas.OtpMethod.EMAIL


class GeneratedSmsOtpEvent(GeneratedOtpEvent):
    """
    GeneratedSmsOtpEvent.
    """

    kind: user_schemas.OtpMethod = user_schemas.OtpMethod.SMS


class CreatedUserEvent(core.Event):
    """
    CreatedUserEvent.
    """

    user: user_schemas.User
