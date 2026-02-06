from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from typing import Optional

async_redis: Redis | None = None
sync_redis: Redis | None = None

def get_async_redis() -> Optional[AsyncRedis]:
    return async_redis

def get_sync_redis() -> Optional[Redis]:
    return sync_redis
