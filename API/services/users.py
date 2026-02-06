from datetime import timedelta
from functools import lru_cache
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from API.utils.verification_code import create_verification_code as generate
from API.responses.response import response
from API.config import current_time
from API.services.base import BaseService
from API.schemas.users import UserSchema
from API.dependencies.JWT.jwt_handler import JWTHandler
from API.dependencies.JWT.jwt_bearer import JWTTokenTypes

from db.postgres.repositories.users import (
    AsyncUserRepository, get_async_user_repo
)
from db.postgres.handlers import create_async_session
from db.schemas import UsersTable


class UserService(BaseService):
    def __init__(self, storage: AsyncUserRepository, session: AsyncSession) -> None:
        super().__init__(storage=storage, session=session)
        self.storage.session = self.session

    async def get_data_by_id(self, *args, **kwargs):
        pass

    async def get_data_list(self, *args, **kwargs):
        return await super().get_data_list(*args, **kwargs)
    
    async def search_data(self, *args, **kwargs):
        return await super().search_data(*args, **kwargs)
    
    async def create_user(self, data: dict):
        result = await AsyncUserRepository(self.session).create_user(data)

        if result and "error" in result:
            return response(
                message="Пользователь уже существует",
                success=False,
                errors={"user": "Пользователь с таким номером телефона уже существует"},
                status_code=status.HTTP_409_CONFLICT
            )

        user_obj = await AsyncUserRepository(self.session).get_user_by_tg_id(
            tg_id=data.get("tg_id")
        )
        return response(
            message="Пользователь успешно создан",
            success=True,
            data={"user": user_obj},
            status_code=status.HTTP_201_CREATED
        )

    async def get_user_by_tg_id(self, tg_id: str):
        user = await AsyncUserRepository(self.session).get_user_by_tg_id(tg_id=str(tg_id))
        if not user:
            return response(
                message="Пользователь не найден",
                success=False,
                errors={"tg_id": "Нет пользователя с таким номером телефона"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return response(
            message="Пользователь успешно извлечен",
            success=True,
            data={"user": user},
            status_code=status.HTTP_200_OK
        )
    
    async def get_user(self, user_id: int):
        user = await AsyncUserRepository(self.session).get(conditions={"id": user_id})
        if not user:
            return response(
                message="Пользователь не найден",
                success=False,
                errors={"id": "Нет пользователя с таким номером телефона"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return response(
            message="Пользователь успешно извлечен",
            success=True,
            data={"user": user},
            status_code=status.HTTP_200_OK
        )
    
    async def authenticate(self, tg_id: str):
        user = await AsyncUserRepository(self.session).authenticate(tg_id=str(tg_id))
        if not user:
            return response(
                message="Недействительные учетные данные",
                success=False,
                errors={"auth": "Неверный Telegram ID"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token_data = {"sub": str(user.id)}
        jwt_handler = JWTHandler(data=token_data)

        access_token = await jwt_handler.create_token(token_type=JWTTokenTypes.access)
        refresh_token = await jwt_handler.create_token(token_type=JWTTokenTypes.refresh)

        return response(
            message="Login successful",
            data={
                "user": user,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status_code=status.HTTP_200_OK,
        )
    
    async def edit_user(self, user: UserSchema, data: dict):
        await AsyncUserRepository(self.session).update(conditions={"id": user.id}, values=data)
        return "changed"


@lru_cache
def get_user_service(
    session: AsyncSession = Depends(create_async_session),
    storage: AsyncUserRepository = Depends(get_async_user_repo)
) -> UserService:
    return UserService(storage=storage, session=session)

