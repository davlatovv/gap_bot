from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
from text import create_group, join_group, start, list_members, info, settings, complain, choose_gap, my_gap


def menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(create_group)),
                KeyboardButton(text=_(join_group))
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
                KeyboardButton(text="Другой день"),
                KeyboardButton(text="Назад"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def menu_for_create():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(start))
            ],
            [
                KeyboardButton(text=_(list_members)),
                KeyboardButton(text=_(info)),
                KeyboardButton(text=_(settings))
            ],
            [
                KeyboardButton(text=_(complain)),
                KeyboardButton(text=_(choose_gap)),
                KeyboardButton(text=_(my_gap))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def menu_for_join():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="список участников"),
                KeyboardButton(text="общая информация"),
                KeyboardButton(text="настройки")
            ],
            [
                KeyboardButton(text="выбор круга"),
                KeyboardButton(text="мои круги")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def accept():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅"),
                KeyboardButton(text="❌")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard







