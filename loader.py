import secrets
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from middlewares.language_middleware import setup_middleware
from data import config
from utils.db_api.database import db

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

__all__ = ["bot", "storage", "dp", "db"]

i18n = setup_middleware(dp)
_ = i18n.gettext


def is_date_greater_than_today(date_string):
    try:
        input_date = datetime.strptime(date_string, "%d/%m/%Y").date()
        today = datetime.now().date()
        if input_date > today:
            return True
        else:
            return False
    except ValueError:
        return False

