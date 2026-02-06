from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis as AsyncRedis
from redis import Redis

from data.config import PostgresSettings, RedisSettings
from API.routers import load_routers
from API.config import current_time
from db import postgres, redis
from db.postgres import factory

psql_settings = PostgresSettings()
redis_settings = RedisSettings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres.async_engine = create_async_engine(
        psql_settings.async_connector,
        pool_pre_ping = True, pool_size = 20, pool_timeout = 30
    )

    postgres.sync_engine = create_engine(
        psql_settings.sync_connector,
        poolclass = QueuePool,
        pool_pre_ping = True, pool_size = 20, pool_timeout = 30
    )
    
    redis.async_redis = AsyncRedis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=redis_settings.db_telegram_fsm,
        decode_responses=True,
        encoding='utf-8'
    )
    
    redis.sync_redis = Redis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=redis_settings.db_custom_data,
        encoding='utf-8'
    )

    factory.async_session_factory = sessionmaker(
        postgres.async_engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession
    )

    factory.sync_session_factory = sessionmaker(
        postgres.sync_engine,
        expire_on_commit=False,
        autoflush=True,
    )

    yield
    await postgres.async_engine.dispose()
    postgres.sync_engine.dispose()
    
    factory.async_session_factory.close_all()
    factory.sync_session_factory.close_all()
    
    await redis.sync_redis.close()
    await redis.async_redis.close()

app = FastAPI(
    title="CIHEVO API", 
    version="1.0.0", 
    description="This API is created for CIHEVO",
    lifespan=lifespan
)

origins = [
    "http://localhost:4444",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/datetime/now")
def datetime_now():
    return current_time()


for router in load_routers():
    app.include_router(
        router = router.router,
        prefix = router.prefix,
        tags = router.tags
    )