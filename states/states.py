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
    members = State()
    location = State()
    link = State()
    start = State()
    period = State()
    private = State()
    accept = State()
    token = State()

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
