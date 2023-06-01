from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
from text import create_group


def menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(create_group)),
                KeyboardButton(text="Присоедениться")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def money():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="100к"),
                KeyboardButton(text="200к"),
                KeyboardButton(text="300к"),
            ],
            [
                KeyboardButton(text="500к"),
                KeyboardButton(text="1000к"),
                KeyboardButton(text="2000к")
            ],
            [
                KeyboardButton(text="Другая сумма"),
                KeyboardButton(text="Назад"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def period():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Раз в неделю"),
                KeyboardButton(text="Раз в в месяц"),
            ],
            [
                KeyboardButton(text="Другая сумма"),
                KeyboardButton(text="Назад"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard




