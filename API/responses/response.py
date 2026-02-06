from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional

def response(
    message: str,
    success: bool = True,
    data: Optional[Any] = None,
    status_code: int = 200,
    errors: Optional[dict] = None,
):
    content = {
        "message": message,
        "success": success,
    }

    if data is not None:
        content["data"] = data

    if errors is not None:
        content["errors"] = errors

    return JSONResponse(content=jsonable_encoder(content), status_code=status_code)