from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from data.config import LANGUAGES
from handlers.users.create_group import choose_name
from handlers.users.join_to_group import join_group
from keyboards.default import get_language_keyboard
from keyboards.default.menu import menu, accept, money, menu_for_join, menu_for_create
from loader import dp, _
from states.states import UserRegistry, CreateGroup, JoinToGroup
from text import user_language, user_name, user_phone, contact, confirm_number, accept_registration, \
    main_menu, yes, no, refuse_registration, create_group, join_group, choose_from_button, right_sms, wrong_sms, \
    create_back, join_back
from utils.db_api.db_commands import DBCommands


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    if await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group_id) is True:
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    elif await DBCommands.get_join(message.from_user.id, group_id=group_id) is True:
        await message.answer(_(main_menu), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    elif await DBCommands.get_user(message.from_user.id):
        await message.answer(_(main_menu), reply_markup=(menu()))
        await state.set_state(UserRegistry.choose)
    else:
        await message.answer(_(user_language), reply_markup=get_language_keyboard())
        await state.update_data(user_id=message.from_user.id, nickname=message.from_user.username)
        await state.set_state(UserRegistry.user_name)


@dp.message_handler(text=[button_text for button_text in LANGUAGES.keys()], state=UserRegistry.user_name)
async def authorization_lang(message: Message, state: FSMContext):
    await message.answer(_(user_name), reply_markup=ReplyKeyboardRemove())
    language = LANGUAGES[message.text]
    await state.update_data(language=language)
    await state.set_state(UserRegistry.user_phone)


@dp.message_handler(state=UserRegistry.user_phone)
async def authorization_name(message: Message, state: FSMContext):
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_(contact), request_contact=True)],
        ],
        resize_keyboard=True
    )
    await state.update_data(name=message.text)
    await message.answer(_(user_phone), reply_markup=contact_keyboard)
    await state.set_state(UserRegistry.user_sms)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegistry.user_sms)
async def authorization_phone(message: Message, state: FSMContext):
    await message.answer(text=_(confirm_number), reply_markup=ReplyKeyboardRemove())
    # send sms phone number
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(UserRegistry.user_sms_accept)


@dp.message_handler(state=UserRegistry.user_sms_accept)
async def accept_sms(message: Message, state: FSMContext):
    if message.text == "1":
        await message.answer("Теперь вам нужно подтвердить пользовательское соглашение", reply_markup=accept())
        await state.update_data(sms=message.text)
        await state.set_state(UserRegistry.user_approve)
    else:
        await message.answer(_(wrong_sms))
        await state.set_state(UserRegistry.user_sms_accept)


@dp.message_handler(state=UserRegistry.user_approve)
async def approve(message: Message, state: FSMContext):
    if message.text == yes:
        data = await state.get_data()
        await DBCommands.create_user(user_id=data.get("user_id"),
                                     name=data.get("name"),
                                     nickname=data.get("nickname"),
                                     phone=data.get("phone"),
                                     language=data.get("language"),
                                     sms=int(data.get("sms")),
                                     accept=1)
        await message.answer(_(accept_registration), reply_markup=menu())
        await state.set_state(UserRegistry.choose)
    elif message.text == no:
        await message.answer(_(refuse_registration), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(_(choose_from_button))


@dp.message_handler(state=UserRegistry.choose)
async def choose_menu(message: Message, state: FSMContext):
    if message.text == create_group:
        await choose_name(message, state)
    elif message.text == join_group:
        await message.answer("Введите токен для присоеденения", reply_markup=ReplyKeyboardRemove())
        await state.set_state(JoinToGroup.join)
    elif message.text == _(create_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    elif message.text == _(join_back):
        await message.answer(_(main_menu), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    else:
        await message.answer(_(choose_from_button))



