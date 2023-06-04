from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.menu import money, period, accept, menu_for_create
from loader import dp, random_token, _
from states.states import CreateGroup
from text import take_period, back, your_token, check_info, my_gap, start, list_members, \
    info, complain, choose_gap, settings, choose_from_button, take_money, take_members, take_name


@dp.message_handler(state=CreateGroup.name)
async def choose_name(message: Message, state: FSMContext):
    await message.answer(_(take_name))
    await state.update_data(name=message.text)
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.money)
async def choose_money(message: Message, state: FSMContext):
    await message.answer(_(take_money), reply_markup=money())
    await state.update_data(money=message.text)
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.period)
async def choose_period(message: Message, state: FSMContext):
    await message.answer(_(take_period), reply_markup=period())
    await state.update_data(money=message.text)
    await state.set_state(CreateGroup.members)


@dp.message_handler(state=CreateGroup.members)
async def choose_members(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton(_(back))
    keyboard.add(back_button)
    await message.answer(_(take_members), reply_markup=keyboard)
    await state.update_data(period=message.text)
    await state.set_state(CreateGroup.accept)


@dp.message_handler(state=CreateGroup.accept)
async def validation(message: Message, state: FSMContext):
    await message.answer(_(check_info), reply_markup=accept())
    await state.update_data(member=message.text)
    await state.set_state(CreateGroup.token)


@dp.message_handler(state=CreateGroup.token)
async def get_token(message: Message, state: FSMContext):
    await message.answer(_(your_token) + random_token, reply_markup=menu_for_create())
    await state.update_data(token=message.text)
    await state.set_state(CreateGroup.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''


@dp.message_handler(state=CreateGroup.choose)
async def choose(message: Message, state: FSMContext):
    if message.text in actions:
        action, new_state = actions[message.text]
        await action(message, state)
        await state.set_state(new_state)
    else:
        await message.answer(_(choose_from_button))


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''


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
