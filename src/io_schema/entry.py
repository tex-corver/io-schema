import pydantic

__all__ = ["Entry"]


class Entry(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        extra="ignore",
    )

    action_type: str | None = None
    url: str
    method: str
    timestamp: int
    user: str
    dataset_before: dict | None = {}
    dataset_after: dict | None = {}
    status: str
    error: str | None = None
    error_message: str | None = None
    error_traceback: str | None = None
