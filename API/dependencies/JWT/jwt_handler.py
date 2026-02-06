from time import time
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from API.config import jwt_settings
from datetime import timedelta

class JWTHandler:
    def __init__(self, data: dict = None):
        self.data = data

    async def decode_jwt(self, token: str):
        try:
            decoded_token = jwt.decode(
                token,
                key=jwt_settings.secret_key,
                algorithms=[jwt_settings.algorithm]
            )
            return decoded_token if decoded_token.get("exp", 0) >= time() else None
        except (ExpiredSignatureError, JWTError):
            return None

    async def create_token(self, token_type: str):
        expires_delta = timedelta(
            minutes = jwt_settings.access_token_expire_minutes
        ) if token_type == 'access_token' else (timedelta(
            days = jwt_settings.refresh_token_expire_days
        ) if token_type == 'refresh_token' else None)
        
        if not self.data or not expires_delta:
            return None
        
        expire_time = int(time() + expires_delta.total_seconds())
        to_encode = self.data.copy()
        to_encode.update({"exp": expire_time, "type": token_type})
        encoded_jwt = jwt.encode(
            to_encode,
            key=jwt_settings.secret_key,
            algorithm=jwt_settings.algorithm
        )
        return encoded_jwt
