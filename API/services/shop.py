import os
import aiofiles
from functools import lru_cache
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from API.services.base import BaseService
from data.config import MEDIA_ROOT
from db.postgres.repositories.shop import AsyncProductRepository, get_async_product_repo
from db.postgres.handlers import create_async_session


async def create_category_image_dir(filename):
    file_dir = f'categories/'
    
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
        
    file_dir_for_django = f'{file_dir}{filename}'
    file_full_path = f"{MEDIA_ROOT}/" + file_dir_for_django
    
    return {
        'file_dir': file_dir_for_django,
        'file_full_path': file_full_path
    }

async def create_brand_image_dir(filename):
    file_dir = f'brands/'
    
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
        
    file_dir_for_django = f'{file_dir}{filename}'
    file_full_path = f"{MEDIA_ROOT}/" + file_dir_for_django
    
    return {
        'file_dir': file_dir_for_django,
        'file_full_path': file_full_path
    }

async def create_product_photo_image_dir(filename):
    file_dir = f'products/'
    
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
        
    file_dir_for_django = f'{file_dir}{filename}'
    file_full_path = f"{MEDIA_ROOT}/" + file_dir_for_django
    
    return {
        'file_dir': file_dir_for_django,
        'file_full_path': file_full_path
    }

class ProductService(BaseService):
    def __init__(self, storage: AsyncProductRepository, session: AsyncSession) -> None:
        super().__init__(storage=storage, session=session)
        self.storage.session = self.session

    async def get_data_by_id(self, *args, **kwargs):
        pass

    async def get_data_list(self, *args, **kwargs):
        return await super().get_data_list(*args, **kwargs)
    
    async def search_data(self, *args, **kwargs):
        return await super().search_data(*args, **kwargs)
    
    async def get_products(self):
        return await AsyncProductRepository(self.session).get_products()
    
    async def filter_products(self, data):
        return await AsyncProductRepository(self.session).filter_products(data)

    async def get_product(self, id: int):
        return await AsyncProductRepository(self.session).get_product(id=id)
    
    async def get_categories(self):
        return await AsyncProductRepository(self.session).get_categories()

@lru_cache
def get_product_service(
    session: AsyncSession = Depends(create_async_session),
    storage: AsyncProductRepository = Depends(get_async_product_repo)
) -> ProductService:
    return ProductService(storage=storage, session=session)

