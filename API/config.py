import datetime
import pytz

from data.config import APISettings, JWTSettings
from fastapi import APIRouter

api_settings = APISettings()
jwt_settings = JWTSettings()


tashkent_tz = pytz.timezone('Asia/Tashkent')

class Versions:
    v1 = '/v1'

class RouterSettings:
    def __init__(self, router: APIRouter, prefix: str, tags: list):
        self.router: APIRouter = router
        self.prefix: str = prefix
        self.tags: list = tags

def current_time(time_zone=True):
    if time_zone:
        return datetime.datetime.now(tz=tashkent_tz)
    else:
        return datetime.datetime.now()