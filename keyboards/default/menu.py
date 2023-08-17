from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("👥Создать круг")),
                KeyboardButton(text=_("👤Присоединиться"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def setting():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆔Изменить имя"),
                KeyboardButton(text="📅Изменить дату встречи")
            ],
            [
                KeyboardButton(text="📅Изменить периодичность"),
                KeyboardButton(text="📎Изменить линк")
            ],
            [
                KeyboardButton(text="📍Изменить локацию"),
                KeyboardButton(text="🌐Изменить язык")
            ],
            [
                KeyboardButton(text="⬅️Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def setting_uz():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆔Nomini o'zgartirish"),
                KeyboardButton(text="📅Uchrashuv sanasini o'zgartirish")
            ],
            [
                KeyboardButton(text="📅Davriylikni o’zgartirish"),
                KeyboardButton(text="📎Havolani o'zgartirish")
            ],
            [
                KeyboardButton(text="📍Joylashuvni o'zgartirish"),
                KeyboardButton(text="🌐Tilni o'zgartiring")
            ],
            [
                KeyboardButton(text="⬅️Orqaga")
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
                KeyboardButton(text=_("➡️Другая сумма")),
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
                KeyboardButton(text=_("➡️Раз в неделю")),
                KeyboardButton(text=_("➡️Раз в месяц")),
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
    keyboard.add(KeyboardButton(text=_("➡️Старт")))
    keyboard.add(KeyboardButton(text=_("📜Список участников")), KeyboardButton(text=_("📋Общая информация")),
                 KeyboardButton(text=_("🎛Настройки")))
    keyboard.add(KeyboardButton(text=_("🆘Пожаловаться")), KeyboardButton(text=_("🔍Выбор круга")),
                 KeyboardButton(text=_("👥Мои круги")))
    return keyboard


def menu_for_create_without_start():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("📜Список участников")), KeyboardButton(text=_("📋Общая информация")), KeyboardButton(text=_("🎛Настройки")))
    keyboard.add(KeyboardButton(text=_("🆘Пожаловаться")), KeyboardButton(text=_("🔍Выбор круга")),
                 KeyboardButton(text=_("👥Мои круги")))
    return keyboard


def menu_for_join():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📜Список участников")),
                KeyboardButton(text=_("📋Общая информация")),
            ],
            [
                KeyboardButton(text=_("🆘Пожаловаться")),
                KeyboardButton(text=_("🔍Выбор круга")),
                KeyboardButton(text=_("👥Мои круги"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def join_choose():
    keyboards = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("➡️Войти по токену")),
                KeyboardButton(text=_("👤Войти в открытые круги"))
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
                KeyboardButton(text=_("📍Отправить текущую локацию"), request_location=True)
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
                KeyboardButton(text=_("🔒Закрытый")),
                KeyboardButton(text=_("🔓Открытый"))
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














