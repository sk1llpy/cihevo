from fastapi import HTTPException, status

token_invalid_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid or Expired Token!"
)

user_not_permitted = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Not enough permission"
)

user_is_banned = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User account is banned."
)

user_is_not_verified = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not verified."
)