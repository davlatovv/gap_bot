from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistry(StatesGroup):
    user_name = State()
    user_phone_and_sms = State()
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
    list_members_to = State()
    list_members_save = State()
    info = State()
    settings = State()
    settings_to = State()
    settings_save = State()
    my_group = State()
    my_group_to = State()
    choose_group = State()
    choose = State()
    complain = State()
    complain_to = State()


class JoinToGroup(StatesGroup):
    join = State()
    join_token = State()
    join_open = State()
    choose = State()
    list_members = State()
    list_members_to = State()
    list_members_save = State()
    info = State()
    complain = State()
    complain_to = State()
    my_group = State()
    my_group_to = State()
    choose_group = State()


class Subscribe(StatesGroup):
    subscribe = State()





