from API.schemas.base import BaseSchema
from pydantic import Field

class AddCartSchema(BaseSchema):
    product_id: int = Field(..., title="product_id")
    size: str | None = Field(..., title="size")
    
class AddSavedProductSchema(BaseSchema):
    product_id: int = Field(..., title="product_id")
