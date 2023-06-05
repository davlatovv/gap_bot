import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType

from keyboards.default.menu import money, period, accept, menu_for_create, location, private
from loader import dp, random_token, _
from states.states import CreateGroup
from text import back, your_token, check_info, my_gap, start, list_members, \
    info, complain, choose_gap, settings, choose_from_button, send_money, send_members, send_name, send_location, \
    send_link, send_start, send_period, send_private
from utils.db_api.db_commands import DBCommands

'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REGISTRATION GAP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.name)
async def choose_name(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton(_(back))
    keyboard.add(back_button)
    await message.answer(_(send_name))
    await state.set_state(CreateGroup.money)


@dp.message_handler(state=CreateGroup.money)
async def choose_money(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton(_(back))
    keyboard.add(back_button)
    await message.answer(_(send_money), reply_markup=money())
    await state.update_data(name=message.text)
    await state.set_state(CreateGroup.members)


@dp.message_handler(state=CreateGroup.members)
async def choose_members(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton(_(back))
    keyboard.add(back_button)
    await message.answer(_(send_members), reply_markup=keyboard)
    await state.update_data(money=message.text)
    await state.set_state(CreateGroup.location)


@dp.message_handler(state=CreateGroup.location)
async def choose_location(message: Message, state: FSMContext):
    await message.answer(_(send_location), reply_markup=location())
    await state.update_data(members=int(message.text))
    await state.set_state(CreateGroup.link)


@dp.message_handler(state=CreateGroup.link, content_types=ContentType.LOCATION)
async def choose_link(message: Message, state: FSMContext):
    await message.answer(_(send_link))
    await state.update_data(location=json.dumps({'latitude': message.location.latitude, 'longitude': message.location.longitude}))
    await state.set_state(CreateGroup.start)


@dp.message_handler(state=CreateGroup.start)
async def choose_start(message: Message, state: FSMContext):
    await message.answer(_(send_start), reply_markup=money())
    await state.update_data(link=message.text)
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.period)
async def choose_period(message: Message, state: FSMContext):
    await message.answer(_(send_period), reply_markup=period())
    await state.update_data(start=message.text)
    await state.set_state(CreateGroup.private)


@dp.message_handler(state=CreateGroup.private)
async def choose_private(message: Message, state: FSMContext):
    await message.answer(_(send_private), reply_markup=private())
    await state.update_data(period=message.text)
    await state.set_state(CreateGroup.accept)


@dp.message_handler(state=CreateGroup.accept)
async def validation(message: Message, state: FSMContext):
    await message.answer(_(check_info), reply_markup=accept())
    if message.text == "Открытый":
        await state.update_data(private=1)
    elif message.text == "Закрытый":
        await state.update_data(private=0)
    else:
        await message.answer(_(choose_from_button))
    await state.update_data(token=random_token)
    await state.set_state(CreateGroup.token)


@dp.message_handler(state=CreateGroup.token)
async def get_token(message: Message, state: FSMContext):
    data = await state.get_data()
    await DBCommands.create_group(user_id=message.from_user.id,
                                  name=data.get('name'),
                                  members=data.get('members'),
                                  money=data.get('money'),
                                  location=data.get('location'),
                                  start=data.get('start'),
                                  period=data.get('period'),
                                  link=data.get('link'),
                                  private=data.get('private'),
                                  token=data.get('token')
                                  )
    await DBCommands.add_member(member=message.from_user.id)
    await message.answer(_(your_token) + data.get('token'), reply_markup=menu_for_create())
    await state.set_state(CreateGroup.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.choose)
async def choose(message: Message, state: FSMContext):
    if message.text in actions:
        action, new_state = actions[message.text]
        await action(message, state)
    else:
        await message.answer(_(choose_from_button))


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.start)
async def start_func(message: Message, state: FSMContext):
    await message.answer("hello")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.list_members)
async def list_members_func(message: Message, state: FSMContext):
    await message.answer("list_members")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.info)
async def info_func(message: Message, state: FSMContext):
    await message.answer("info")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.settings)
async def settings_func(message: Message, state: FSMContext):
    await message.answer("settings")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.complain)
async def complain_func(message: Message, state: FSMContext):
    await message.answer("complain")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.choose_gap)
async def choose_gap_func(message: Message, state: FSMContext):
    await message.answer("choose_gap")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.my_gap)
async def my_gap_func(message: Message, state: FSMContext):
    await message.answer("my_gap")
    await state.set_state(CreateGroup.choose)


actions = {
    _(start): (start_func, CreateGroup.start),
    _(list_members): (list_members_func, CreateGroup.list_members),
    _(info): (info_func, CreateGroup.info),
    _(settings): (settings_func, CreateGroup.settings),
    _(complain): (complain_func, CreateGroup.complain),
    _(choose_gap): (choose_gap_func, CreateGroup.choose_gap),
    _(my_gap): (my_gap_func, CreateGroup.my_gap)
}
