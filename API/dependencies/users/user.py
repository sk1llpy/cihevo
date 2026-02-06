from fastapi import Depends
from jose import JWTError

from API.dependencies.JWT.jwt_handler import JWTHandler
from API.dependencies.JWT.jwt_bearer import JwtBearer
from API.exceptions.exception import user_not_permitted, user_is_banned, user_is_not_verified, token_invalid_exception
from API.queries.users import UserQuery
from API.schemas.users import UserSchema


class UserHandling:
    def __init__(self) -> None:
        pass

    async def user(self, token: str = Depends(JwtBearer())):
        try:
            payload = await JWTHandler().decode_jwt(token)
            user = await UserHandling.determine_user(payload=payload)
            user_schema = UserSchema(**(await user).__dict__)
            
            return user_schema
        except JWTError:
            raise token_invalid_exception

    @staticmethod
    async def determine_user(payload: dict):
        user_id: int = int(payload.get("sub"))
        
        user = UserQuery().user(user_id = user_id)
        
        return user

    async def token_data(self, token: str = Depends(JwtBearer())):
        try:
            payload = await JWTHandler().decode_jwt(token)
            return payload
        except JWTError:
            raise ValueError("Invalid username or password")
