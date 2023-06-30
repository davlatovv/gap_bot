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
    menu = State()

    list_members = State()
    info = State()
    settings = State()
    my_gap = State()
    my_gap_to = State()
    choose_gap = State()
    choose = State()
    complain = State()
    complain_to = State()


class JoinToGroup(StatesGroup):
    join = State()
    choose = State()
    list_members = State()
    info = State()
    complain = State()
    choose_gap = State()
    my_gap = State()
    my_gap_to = State()




