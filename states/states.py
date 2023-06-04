from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistry(StatesGroup):
    user_name = State()
    user_phone = State()
    user_sms = State()
    user_sms_accept = State()
    user_approve = State()
    choose = State()


class CreateGroup(StatesGroup):
    name = State()
    money = State()
    period = State()
    members = State()
    accept = State()
    token = State()
    start = State()
    list_members = State()
    info = State()
    settings = State()
    my_gap = State()
    choose_gap = State()
    choose = State()
    complain = State()


class JoinToGroup(StatesGroup):
    join = State()
    menu = State()
