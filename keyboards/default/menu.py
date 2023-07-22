from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text import *
from loader import _


def menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Создать круг")),
                KeyboardButton(text=_("Присоедениться"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def setting():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Изменить имя")),
                KeyboardButton(text=_("Изменить дату встречи"))
            ],
            [
                KeyboardButton(text=_("Изменить переодичность")),
                KeyboardButton(text=_("Изменить линк"))
            ],
            [
                KeyboardButton(text=_("Изменить локацию")),
                KeyboardButton(text=_("Изменить язык"))
            ],
            [
                KeyboardButton(text=_("⬅️Назад"))
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
                KeyboardButton(text=_("Другая сумма")),
                KeyboardButton(text=_("⬅️Назад")),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def period():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Раз в неделю")),
                KeyboardButton(text=_("Раз в в месяц")),
            ],
            [
                KeyboardButton(text=_("⬅️Назад")),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def menu_for_create():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Старт")))
    keyboard.add(KeyboardButton(text=_("Список участников")), KeyboardButton(text=_("Общая информация")),
                 KeyboardButton(text=_("Настройки")))
    keyboard.add(KeyboardButton(text=_("Пожаловаться")), KeyboardButton(text=_("Выбор круга")),
                 KeyboardButton(text=_("Мои круги")))
    return keyboard


def menu_for_create_without_start():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Список участников")), KeyboardButton(text=_("Общая информация")), KeyboardButton(text=_("Настройки")))
    keyboard.add(KeyboardButton(text=_("Пожаловаться")), KeyboardButton(text=_("Выбор круга")),
                 KeyboardButton(text=_("Мои круги")))
    return keyboard


def menu_for_join():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Список участников")),
                KeyboardButton(text=_("Общая информация")),
            ],
            [
                KeyboardButton(text=_("Пожаловаться")),
                KeyboardButton(text=_("Выбор круга")),
                KeyboardButton(text=_("Мои круги"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def join_choose():
    keyboards = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Войти по токену")),
                KeyboardButton(text=_("Войти в открытые круги"))
            ],
            [
                KeyboardButton(text=_("Назад ⬅️"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboards


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


def location():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Отправить текущую локацию"), request_location=True)
            ],
            [
                KeyboardButton(text=_("⬅️Назад"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def private():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Закрытый")),
                KeyboardButton(text=_("Открытый"))
            ],
            [
                KeyboardButton(text=_("⬅️Назад"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def back_state():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("⬅️Назад"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard














