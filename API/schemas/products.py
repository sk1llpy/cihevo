from API.schemas.base import BaseSchema
from pydantic import Field

class FilterSchema(BaseSchema):
    size: list = Field(..., title="size")
    categories: list | None = Field(..., title="categories")
    in_stock: bool | None = Field(..., title="in_stock")
    out_of_stock: bool | None = Field(..., title="out_of_stock")
    colors: list | None = Field(..., title="colors")
    min_price: int | None = Field(..., title="min_price")
    max_price: int | None = Field(..., title="max_price")
