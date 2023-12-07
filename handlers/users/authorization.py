from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from data.config import LANGUAGES
from handlers.users.create_group import choose_name
from keyboards.default import get_language_keyboard
from keyboards.default.menu import *
from states.states import UserRegistry, CreateGroup, JoinToGroup, Subscribe
from loader import _, dp
from utils.db_api.db_commands import DBCommands


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    user = await DBCommands.get_user(message.from_user.id)
    if user is not None and user.subscribe == 0:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer(text=_("⚠️Ваше время истекло, теперь приобретите подписку"), reply_markup=keyboard.add(_("🎫ПОДПИСКА")))
        await state.set_state(Subscribe.subscribe)
    elif await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group_id) is True:
        group = await DBCommands.get_group_from_id(group_id=group_id)
        if group.start == 0:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    elif await DBCommands.get_user_from_table_member(message.from_user.id, group_id=group_id):
        await message.answer(_("📱Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    elif user is not None and user.name is not None:
        await message.answer(_("📱Главное меню"), reply_markup=(menu()))
        await state.set_state(UserRegistry.choose)
    else:
        await message.answer(_("🙂Добро пожаловать в “ЧЁРНАЯ КАССА”.\n" 
                "😉Мы поможем вам сделать ваш “Ga’p” более удобным и безопасным!\n\n" 
                "🙂“ЧЁРНАЯ КАССА” ga xush kelibsiz.\n"
                "😉Biz sizga “Ga’p” ni qulayroq va xavfsizroq qilishingizga yordam beramiz!\n\n"
                "🇷🇺Для начала выберите удобный вам язык!\n" 
                "🇺🇿Ўзингизга қулай тилни танланг!\n"), reply_markup=get_language_keyboard())
        await state.update_data(user_id=message.from_user.id, nickname=message.from_user.username)
        await state.set_state(UserRegistry.user_name)


@dp.message_handler(text=[button_text for button_text in LANGUAGES.keys()], state=UserRegistry.user_name)
async def authorization_lang(message: Message, state: FSMContext):
    language = LANGUAGES[message.text]
    user = await DBCommands.get_user(message.from_user.id)
    if not user:
        await DBCommands.add_language(message.from_user.id, language)
    if user:
        await DBCommands.language_update(message.from_user.id, language)
    if message.text == "🇷🇺 Русский":
        await message.answer("👨‍💻Введите пожалуйста свое ФИО, пример: (Шукуров Нурбек Туробович)",
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == "🇺🇿 Ўзбек тили":
        await message.answer("👨‍💻Iltimos, to'liq ismingizni kiriting, misol: (Shukurov Nurbek Turobovich)",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("❇️Выберите одну из кнопок\n❇️Tugmalardan birini tanlang")
        await state.set_state(UserRegistry.user_name)
    await state.set_state(UserRegistry.user_phone_and_sms)


# @dp.message_handler(state=UserRegistry.user_phone)
# async def authorization_name(message: Message, state: FSMContext):
#     contact_keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text=_("☎️Ваш контакт"), request_contact=True)],
#         ],
#         resize_keyboard=True
#     )
#     await state.update_data(name=message.text)
#     await message.answer(_("📲Поделитесь своим контактом,нажав на кнопку ниже:"), reply_markup=contact_keyboard)
#     await state.set_state(UserRegistry.user_sms)


@dp.message_handler(state=UserRegistry.user_phone_and_sms)
async def authorization_phone(message: Message, state: FSMContext):
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("☎️Ваш контакт"), request_contact=True)],
        ],
        resize_keyboard=True
    )
    await state.update_data(name=message.text)
    await message.answer(_("Ознакомьтесь с пользовательским соглашением и подтвердите его нажав на кнопку 'поделиться контактом'!\n"
                           "⚠️Предупреждение:подтверждая пользовательское соглашение вы принимаете на себя ответственность за свои действия!\n"
                           "📕Пользовательское соглашение:"))
    await message.answer_document(open("/home/documents/ПОЛЬЗОВАТЕЛЬСКОЕ_СОГЛАШЕНИЕ_MATES.docx", 'rb'))
    await state.set_state(UserRegistry.user_approve)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegistry.user_approve)
async def approve(message: Message, state: FSMContext):
    # if message.text == "✅":
    data = await state.get_data()
    await DBCommands.create_user(user_id=data.get("user_id"),
                                 name=data.get("name"),
                                 nickname=data.get("nickname"),
                                 phone=message.contact.phone_number,
                                 accept=1)
    await message.answer(_("🎉Поздравляем, вы успешно зарегистрировались!\n" 
                  "Выберите 👥-создать круг- если вы хотите создать свой круг,\n" 
                  "или 👤-присоединиться- если вы хотите присоединиться к уже существующему кругу.\n"), reply_markup=menu())
    await state.set_state(UserRegistry.choose)

@dp.message_handler(state=UserRegistry.choose)
async def choose_menu(message: Message, state: FSMContext):
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    if message.text in ["👥Создать круг", "👥Doira yaratish"]:
        await choose_name(message, state)
    elif message.text in ["👤Присоединиться", "👤Qo'shilish"]:
        await message.answer(_("👤Выберите в какой круг присоединиться"), reply_markup=join_choose())
        await state.set_state(JoinToGroup.join)
    elif message.text in ["⬅️Назад", "⬅️Orqaga"]:
        if group.start == 0:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    elif message.text in ["⬅️ Назад", "⬅️ Orqaga"]:
        await message.answer(_("📱Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    else:
        if group.start == 0:
            await message.answer(_("❇️Выберите одну из кнопок"), reply_markup=menu_for_create())
        else:
            await message.answer(_("❇️Выберите одну из кнопок"), reply_markup=menu_for_create_without_start())
        await state.set_state(UserRegistry.choose)



