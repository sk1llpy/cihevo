import datetime

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import (declarative_base, DeclarativeBase,
                            Session, sessionmaker,
                            Mapped, mapped_column)
from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from uuid import UUID, uuid4
from data.config import PostgresSettings, RedisSettings
from typing_extensions import Annotated


psql = PostgresSettings()

engine: Engine = create_engine(psql.sync_connector)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeBase = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True)]

class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    uuid: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(onupdate=datetime.datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    @property
    def created_at_utc(self) -> datetime.datetime:
        if self.created_at:
            return self.created_at + datetime.timedelta(hours=5)

    @property
    def updated_at_utc(self) -> datetime.datetime:
        if self.updated_at:
            return self.updated_at + datetime.timedelta(hours=5)
