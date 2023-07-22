from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from data.config import LANGUAGES
from handlers.users.create_group import choose_name
from keyboards.default import get_language_keyboard
from keyboards.default.menu import *
from states.states import UserRegistry, CreateGroup, JoinToGroup, Subscribe
from text import *
from loader import _, dp
from utils.db_api.db_commands import DBCommands


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    user = await DBCommands.get_user(message.from_user.id)
    if user is not None and user.subscribe == 0:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer(text=_("Ваше время истекло, теперь приобретите подписку"), reply_markup=keyboard.add(_("ПОДПИСКА")))
        await state.set_state(Subscribe.subscribe)
    elif await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group_id) is True:
        group = await DBCommands.get_group_from_id(group_id=group_id)
        if group.start == 0:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    elif await DBCommands.get_user_from_table_member(message.from_user.id, group_id=group_id):
        await message.answer(_("Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    elif user:
        await message.answer(_("Главное меню"), reply_markup=(menu()))
        await state.set_state(UserRegistry.choose)
    else:
        await message.answer(_("Добро пожаловать в “mates”.\n" 
                "Мы поможем вам сделать ваш “Ga’p” более удобным и безопасным!\n\n" 
                "“mates” ga xush kelibsiz.\n"
                "Biz sizga “Ga’p” ni qulayroq va xavfsizroq qilishingizga yordam beramiz!\n\n"
                "🇷🇺Для начала выберите удобный вам язык!\n" 
                "🇺🇿Ўзингизга қулай тилни танланг!\n"), reply_markup=get_language_keyboard())
        await state.update_data(user_id=message.from_user.id, nickname=message.from_user.username)
        await state.set_state(UserRegistry.user_name)


@dp.message_handler(text=[button_text for button_text in LANGUAGES.keys()], state=UserRegistry.user_name)
async def authorization_lang(message: Message, state: FSMContext):
    await message.answer(user_name, reply_markup=ReplyKeyboardRemove())
    language = LANGUAGES[message.text]
    await state.update_data(language=language)
    await state.set_state(UserRegistry.user_phone)


@dp.message_handler(state=UserRegistry.user_phone)
async def authorization_name(message: Message, state: FSMContext):
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=contact, request_contact=True)],
        ],
        resize_keyboard=True
    )
    await state.update_data(name=message.text)
    await message.answer(user_phone, reply_markup=contact_keyboard)
    await state.set_state(UserRegistry.user_sms)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegistry.user_sms)
async def authorization_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(_("Ознакомьтесь с пользовательским соглашением и подтвердите его!\n" 
                             "Пользовательское соглашение:\n" 
                             "(ссылка на пользовательское соглашение\n" 
                             "Предупреждение:подтверждая пользовательское соглашение вы принимаете на себя ответственность за свои действия!"), reply_markup=accept())
    await message.answer_document(open("document.docx", 'rb'))
    await state.update_data(sms=message.text)
    await state.set_state(UserRegistry.user_approve)


@dp.message_handler(state=UserRegistry.user_approve)
async def approve(message: Message, state: FSMContext):
    if message.text == yes:
        data = await state.get_data()
        await DBCommands.create_user(user_id=data.get("user_id"),
                                     name=data.get("name"),
                                     nickname=data.get("nickname"),
                                     phone=data.get("phone"),
                                     language=data.get("language"),
                                     accept=1)
        await message.answer(_("Поздравляем, вы успешно зарегистрировались!\n" 
                      "Выберите -создать круг- если вы хотите создать свой круг,\n" 
                      "или -присоедениться- если вы хотите присоедениться к уже существующему кругу.\n"), reply_markup=menu())
        await state.set_state(UserRegistry.choose)
    elif message.text == no:
        await message.answer(_("Вы отклонили пользовательское соглашение поэтому мы не сможем продолжить.\n" 
                      "Нажмите /start если хотите заново зарегестрироваться"), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(_("Выберите одну из кнопок"))


@dp.message_handler(state=UserRegistry.choose)
async def choose_menu(message: Message, state: FSMContext):
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    if message.text == _("Создать круг"):
        await choose_name(message, state)
    elif message.text == _("Присоедениться"):
        await message.answer(_("Выберите в какой круг присоедениться"), reply_markup=join_choose())
        await state.set_state(JoinToGroup.join)
    elif message.text == _("⬅️Назад"):
        if group.start == 0:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    elif message.text == _("⬅️ Назад"):
        await message.answer(_("Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    else:
        await message.answer(choose_from_button)



