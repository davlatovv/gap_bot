from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_language_keyboard():
    language_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇷🇺 Русский")
            ],
            [
                KeyboardButton(text="🇺🇿 Ўзбек тили")
            ],
        ],
        resize_keyboard=True
    )

    return language_keyboard
