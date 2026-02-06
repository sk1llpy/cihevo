from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from API.exceptions.exception import token_invalid_exception
from API.dependencies.JWT.jwt_handler import JWTHandler


class JWTTokenTypes:
    access = 'access_token'
    refresh = 'refresh_token'

class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=True)

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super(
            JwtBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise token_invalid_exception
            token_status = await self.verify_jwt(
                jwtoken=credentials.credentials)
            if not token_status:
                raise token_invalid_exception
            return credentials.credentials
        else:
            raise token_invalid_exception

    async def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False
        payload = await JWTHandler().decode_jwt(token=jwtoken)
        if payload:
            is_token_valid = True
        return is_token_valid
