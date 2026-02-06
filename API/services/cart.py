import os
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from API.services.base import BaseService
from db.postgres.repositories.shop import AsyncProductRepository, get_async_product_repo
from db.postgres.handlers import create_async_session


class CartService(BaseService):
    def __init__(self, storage: AsyncProductRepository, session: AsyncSession) -> None:
        super().__init__(storage=storage, session=session)
        self.storage.session = self.session

    async def get_data_by_id(self, *args, **kwargs):
        pass

    async def get_data_list(self, *args, **kwargs):
        return await super().get_data_list(*args, **kwargs)
    
    async def search_data(self, *args, **kwargs):
        return await super().search_data(*args, **kwargs)

    async def get_cart(self, user_id: int):
        return await AsyncProductRepository(self.session).cart(user_id=user_id)
    
    async def get_saved_products(self, user_id: int):
        return await AsyncProductRepository(self.session).saved_products(user_id=user_id)
    
    async def remove_cart(self, user_id: int, cart_id: int):
        return await AsyncProductRepository(self.session).remove_cart(user_id=user_id, cart_id=cart_id)
    
    async def add_to_cart(self, user_id: int, product_id: int, size: str = None):
        return await AsyncProductRepository(self.session).add_to_cart(
            product_id = product_id, 
            user_id = user_id, 
            size = size
        )

    async def add_to_saved(self, user_id: int, product_id: int):
        return await AsyncProductRepository(self.session).add_to_saved(
            product_id = product_id, 
            user_id = user_id
        )
    
    async def remove_saved(self, user_id: int, product_id: int):
        return await AsyncProductRepository(self.session).remove_saved_product(
            product_id = product_id, 
            user_id = user_id
        )

@lru_cache
def get_cart_service(
    session: AsyncSession = Depends(create_async_session),
    storage: AsyncProductRepository = Depends(get_async_product_repo)
) -> CartService:
    return CartService(storage=storage, session=session)
