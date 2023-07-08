from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
from text import *


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


def setting():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(change_name)),
                KeyboardButton(text=_(change_date))
            ],
            [
                KeyboardButton(text=_(change_period)),
                KeyboardButton(text=_(change_link))
            ],
            [
                KeyboardButton(text=_(change_location)),
                KeyboardButton(text=_(create_back))
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
                KeyboardButton(text=_(other_money)),
                KeyboardButton(text=_(create_back)),
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
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_(start)))
    keyboard.add(KeyboardButton(text=_(list_members)), KeyboardButton(text=_(info)),
                 KeyboardButton(text=_(settings)))
    keyboard.add(KeyboardButton(text=_(complain)), KeyboardButton(text=_(choose_group)),
                 KeyboardButton(text=_(my_group)))
    return keyboard


def menu_for_create_without_start():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_(list_members)), KeyboardButton(text=_(info)), KeyboardButton(text=_(settings)))
    keyboard.add(KeyboardButton(text=_(complain)), KeyboardButton(text=_(choose_group)),
                 KeyboardButton(text=_(my_group)))
    return keyboard


def menu_for_join():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(list_members)),
                KeyboardButton(text=_(info)),
            ],
            [
                KeyboardButton(text=_(complain)),
                KeyboardButton(text=_(choose_group)),
                KeyboardButton(text=_(my_group))
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














