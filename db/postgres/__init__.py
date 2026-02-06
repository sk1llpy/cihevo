from abc import ABC, abstractmethod, abstractproperty
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine


class BaseSessionHandler(ABC):
    @abstractmethod
    def session_scope(self):
        pass

    @abstractmethod
    def session(self):
        pass



class BaseSessionFactory(ABC):
    @abstractproperty
    def async_session_maker(self) -> sessionmaker:
        pass
    
    @abstractproperty
    def sync_session_maker(self) -> sessionmaker:
        pass


class BaseDbConnector(ABC):
    @abstractproperty
    def sync_connector(self):
        pass
    
    @abstractproperty
    def async_connector(self):
        pass


async_engine: AsyncEngine | None = None
sync_engine: Engine | None = None

def get_async_engine() -> AsyncEngine | None:
    return async_engine

def get_sync_engine() -> Engine | None:
    return sync_engine
