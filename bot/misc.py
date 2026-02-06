from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from redis.asyncio import Redis

from data.config import BotSettings, RedisSettings

bot_settings = BotSettings()
redis_settings = RedisSettings()

redis = Redis(
    host=redis_settings.host,
    port=redis_settings.port,
    db=redis_settings.db_telegram_fsm,
    decode_responses=True,
    encoding='utf-8'
)
storage = RedisStorage(
    redis = redis
)
dp = Dispatcher(
    storage = storage
)
bot = Bot(
    token = bot_settings.token,
    default = DefaultBotProperties(
        parse_mode = ParseMode.HTML
    )
)