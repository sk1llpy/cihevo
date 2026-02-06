from abc import ABC, abstractmethod
from typing import Any
from db.postgres.repositories import AsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService(ABC):
    def __init__(self, session: AsyncSession = None, storage: AsyncRepository = None) -> None:
        self.storage = storage
        self.session = session

    @abstractmethod
    async def get_data_by_id(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod 
    async def get_data_list(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def search_data(self, *args, **kwargs) -> Any:
        pass
