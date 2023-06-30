import secrets
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup
from datetime import datetime, timedelta
from middlewares.language_middleware import setup_middleware
from data import config
from utils.db_api.database import db

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

__all__ = ["bot", "storage", "dp", "db"]

i18n = setup_middleware(dp)
_ = i18n.gettext

random_token = secrets.token_hex(16)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


def add_days_multiple_times(start_date_str, num_days, members):
    dates = []
    date_format = "%d/%m/%Y"

    start_date = datetime.strptime(start_date_str, date_format)
    dates.append(start_date.strftime(date_format))

    for _ in range(members):
        new_date = start_date + timedelta(days=num_days)
        dates.append(new_date.strftime(date_format))
        start_date = new_date

    return dates



