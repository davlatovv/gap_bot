from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from data.config import LANGUAGES
from keyboards.default import get_language_keyboard
from keyboards.default.menu import menu
from loader import dp, _
from states.states import UserRegistry
from text import user_language, user_name, user_phone, contact, confirm_number, accept_registration, wrong_registration, main_menu
from utils.db_api.db_commands import DBCommands


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    if await DBCommands.get_user(message.from_user.id):
        await message.answer(_(main_menu), reply_markup=(menu()))
        await state.finish()
    else:
        await state.reset_state()
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
    await message.answer(text=_(confirm_number))
    # send sms phone number
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(UserRegistry.user_menu)


@dp.message_handler(state=UserRegistry.user_menu)
async def accept_sms(message: Message, state: FSMContext):
    if message.text == "1":
        data = await state.get_data()
        await DBCommands.create_user(user_id=data.get("user_id"),
                                     name=data.get("name"),
                                     nickname=data.get("nickname"),
                                     phone=data.get("phone"),
                                     language=data.get("language"),
                                     sms=1)
        await state.finish()
        await message.answer(_(accept_registration), reply_markup=menu())
    else:
        await message.answer(_(wrong_registration))
        await state.reset_state()
