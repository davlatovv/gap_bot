from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistry(StatesGroup):
    user_name = State()
    user_phone = State()
    user_sms = State()
    user_accept = State()
    user_menu = State()


class CreateGroup(StatesGroup):
    create = State()
    money = State()


class JoinToGroup(StatesGroup):
    join = State()
