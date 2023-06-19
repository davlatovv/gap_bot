from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
from text import create_group, join_group, start, list_members, info, settings, complain, choose_gap, my_gap, onse_week, \
    onse_month, yes, no, send_location, close, open, create_back


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
                KeyboardButton(text="100.000"),
                KeyboardButton(text="200.000"),
                KeyboardButton(text="300.000"),
            ],
            [
                KeyboardButton(text="500.000"),
                KeyboardButton(text="1.000.000"),
                KeyboardButton(text="2.000.000")
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
                KeyboardButton(text=_(onse_week)),
                KeyboardButton(text=_(onse_month)),
            ],
            [
                KeyboardButton(text=_(create_back)),
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


def accept():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=yes),
                KeyboardButton(text=no)
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def location():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(send_location), request_location=True)
            ],
            [
                KeyboardButton(text=_(create_back))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def private():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(close)),
                KeyboardButton(text=_(open))
            ],
            [
                KeyboardButton(text=_(create_back))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def back_state():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(create_back))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard











