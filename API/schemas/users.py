from API.schemas.base import BaseSchema
from datetime import date
from pydantic import Field

class UserSchema(BaseSchema):
    id: int = None
    first_name: str | None = Field(None, title="first_name")
    last_name: str | None = Field(None, title="last_name")
    phone_number: str | None = Field(None, title="phone_number")
    basket: list | None = Field(None, title="basket")

class VerifyTokenSchema(BaseSchema):
    token: str = Field(..., title="token")
    tg_id: str = Field(..., title="tg_id")
