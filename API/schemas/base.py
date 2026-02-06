from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
