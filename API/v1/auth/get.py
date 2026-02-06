import secrets
import datetime
from fastapi import Depends

from .router import router
from API.services.users import UserService, get_user_service
from API.cache.redis import RedisCache


@router.get("/get-url")
async def get_login_url():
    cache = RedisCache(expire=300)
    token = secrets.token_hex(24)
    expires_at = (datetime.datetime.utcnow() + datetime.timedelta(seconds=30)).isoformat()
    
    await cache.put_to_cache(
        url=f"login_token:{token}",
        data={
            "verified": False,
            "expires_at": expires_at
        }
    )

    telegram_url = f"https://t.me/cihevo_bot?start={token}"
    return {"token": token, "url": telegram_url, "expires_at": expires_at}


@router.get("/login/{token}")
async def login(token: str, service: UserService = Depends(get_user_service)):
    cache = RedisCache(expire=300)
    token_data = await cache.get_from_cache(f"login_token:{token}")
    
    datetime_now = datetime.datetime.utcnow()
    if token_data:
        expires_at = datetime.datetime.fromisoformat(token_data["expires_at"])
        expired = datetime_now > expires_at
        if token_data["verified"]:
            return await service.authenticate(tg_id=token_data.get("user_id"))
        else:
            return {"verified": False, "expired": expired}
    return {"verified": False, "expired": True}
