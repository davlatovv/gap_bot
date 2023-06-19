import secrets
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from middlewares.language_middleware import setup_middleware

from data import config
from states.states import UserRegistry
from utils.db_api.database import db

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

__all__ = ["bot", "storage", "dp", "db"]

i18n = setup_middleware(dp)
_ = i18n.gettext

random_token = secrets.token_hex(16)



