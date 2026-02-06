from fastapi import HTTPException, status

order_by_field_not_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="order by field has wrong field name")

integrity_error = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="record already exists")
