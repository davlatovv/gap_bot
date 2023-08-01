import json
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, \
    InlineKeyboardButton

from data.config import LANGUAGES
from keyboards.default import get_language_keyboard
from keyboards.default.menu import *
from loader import dp, random_token, _, bot, is_date_greater_than_today
from states.states import CreateGroup, UserRegistry, JoinToGroup
from text import *
from utils.db_api.db_commands import DBCommands


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REGISTRATION GROUP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.name)
async def choose_name(message: Message, state: FSMContext):
    await message.answer(_("Назовите свой круг, например: круг коллег."), reply_markup=back_state())
    await state.set_state(CreateGroup.money)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.money)
async def go_back_to_name(message: Message, state: FSMContext):
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    if not group:
        await message.answer(_("Главное меню"), reply_markup=menu())
    elif group.user_id == message.from_user.id:
        await message.answer(_("Главное меню"), reply_markup=menu().add(KeyboardButton(_("⬅️Назад"))))
    else:
        await message.answer(_("Главное меню"), reply_markup=menu().add(KeyboardButton(_("⬅️Назад"))))
    await state.set_state(UserRegistry.choose)


@dp.message_handler(state=CreateGroup.money)
async def choose_money(message: Message, state: FSMContext):
    await message.answer(_("Выберите сумму взносов( эту сумму,каждый из участников будет отдавать получателю вознаграждения:"), reply_markup=money())
    await state.update_data(name=message.text)
    await state.set_state(CreateGroup.members)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.members)
async def go_back_to_money(message: Message, state: FSMContext):
    await message.answer(_("Назовите свой круг, например: круг коллег."), reply_markup=back_state())
    await state.set_state(CreateGroup.money)


@dp.message_handler(state=CreateGroup.members)
async def choose_money(message: Message, state: FSMContext):
    if message.text == _("Другая сумма"):
        await message.answer(_("Введите сумму:"))
        await state.set_state(CreateGroup.members)
    elif message.text.isdigit() or re.match(r'\d{1,3}.\d{1,3}.\d{3}', message.text) or re.match(r'\d{1,3}.\d{3}', message.text):
        await message.answer(_("Введите цифрами количество участников вашего круга, пример: 5"), reply_markup=back_state())
        await state.update_data(money=message.text)
        await state.set_state(CreateGroup.location)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.location)
async def go_back_to_members(message: Message, state: FSMContext):
    await message.answer(_("Выберите сумму взносов( эту сумму,каждый из участников будет отдавать получателю вознаграждения:"), reply_markup=money())
    await state.set_state(CreateGroup.members)


@dp.message_handler(state=CreateGroup.location)
async def choose_members(message: Message, state: FSMContext):
    await message.answer(_("Отправьте локацию места, где вы планируете собираться с участниками:\nCовет:вы можете выбрать локацию вручную или же переслать ее из другого чата."), reply_markup=location())
    if message.text.isdigit():
        await state.update_data(members=message.text)
    else:
        await message.answer(_("Пожалуйста введите цифрами"))
    await state.set_state(CreateGroup.link)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.link)
async def go_back_to_location(message: Message, state: FSMContext):
    await message.answer(_("Введите цифрами количество участников вашего круга, пример: 5"), reply_markup=back_state())
    await state.set_state(CreateGroup.location)


@dp.message_handler(state=CreateGroup.link, content_types=ContentType.LOCATION)
async def choose_location(message: Message, state: FSMContext):
    await message.answer(_("Создайте группу в телеграм и добавьте в нее участников, чьи контакты у вас уже имеются, для остальных отправьте ссылку на группу в которую они могут вступить.\nСовет:ссылку на группу вы можете найти следующим способом(видео записи экрана, как пользователь копирует ссылку группы и отправляет ее боту"), reply_markup=back_state())
    await state.update_data(location=json.dumps({'latitude': message.location.latitude, 'longitude': message.location.longitude}))
    await state.set_state(CreateGroup.start)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.start)
async def go_back_to_link(message: Message, state: FSMContext):
    await message.answer(_("Отправьте локацию места, где вы планируете собираться с участниками:\nCовет:вы можете выбрать локацию вручную или же переслать ее из другого чата."), reply_markup=location())
    await state.set_state(CreateGroup.link)


@dp.message_handler(state=CreateGroup.start)
async def choose_start(message: Message, state: FSMContext):
    await message.answer(_("Отправьте дату начала в следующем формате ДД/ММ/ГГГГ:"), reply_markup=back_state())
    await state.update_data(link=message.text)
    await state.set_state(CreateGroup.period)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.period)
async def go_back_to_start(message: Message, state: FSMContext):
    await message.answer(_("Создайте группу в телеграм и добавьте в нее участников, чьи контакты у вас уже имеются, для остальных отправьте ссылку на группу в которую они могут вступить.\nСовет:ссылку на группу вы можете найти следующим способом(видео записи экрана, как пользователь копирует ссылку группы и отправляет ее боту"
), reply_markup=back_state())
    await state.set_state(CreateGroup.start)


@dp.message_handler(state=CreateGroup.period)
async def choose_period(message: Message, state: FSMContext):
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    if re.match(date_pattern, message.text) and is_date_greater_than_today(message.text) is True:
        await message.answer(_("Выберите, как часто вы планируете собираться:"), reply_markup=period())
        await state.update_data(start=message.text)
        await state.set_state(CreateGroup.private)
    else:
        await message.answer(_("Невереная дата"))


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.private)
async def go_back_to_period(message: Message, state: FSMContext):
    await message.answer(_("Отправьте дату начала в следующем формате ДД/ММ/ГГГГ:"), reply_markup=back_state())
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.private)
async def choose_private(message: Message, state: FSMContext):
    if message.text == _("Раз в неделю"):
        await state.update_data(period=7)
    elif message.text == _("Раз в в месяц"):
        await state.update_data(period=30)
    else:
        if message.text.isdigit():
            await state.update_data(period=message.text)
        else:
            await message.answer(_("Пожалуйста введите цифрами"))
    await message.answer(_("Выберите статус приватности вашего круга:\n"
               "Подсказка: если вы выберете открытый статус, то ваш круг будет виден в общем списке и любой желающий сможет вступить в него. Если вы выберите закрытый статус, для вступления в ваш круг пользователям нужен будет токен."), reply_markup=private())
    await state.set_state(CreateGroup.accept)


@dp.message_handler(text=_("⬅️Назад"), state=CreateGroup.accept)
async def go_back_to_period(message: Message, state: FSMContext):
    await message.answer(_("Выберите, как часто вы планируете собираться:"), reply_markup=period())
    await state.set_state(CreateGroup.private)


@dp.message_handler(state=CreateGroup.accept)
async def validation(message: Message, state: FSMContext):
    if message.text == "Открытый":
        await state.update_data(private=1)
    elif message.text == "Закрытый":
        await state.update_data(private=0)
    else:
        await message.answer(_("Выберите одну из кнопок"))
    data = await state.get_data()
    await message.answer("Имя круга: " + str(data.get('name')) + "\n" +
                         "Число участников: " + str(data.get('members')) + "\n" +
                         "Сумма: " + str(data.get('money')) + "\n" +
                         "Дата начала: " + str(data.get('start')) + "\n" +
                         "Переодичность: " + str(data.get('period')) + "\n" +
                         "Линк: " + str(data.get('link')) + "\n" +
                         "Приватность: " + message.text + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(data.get('location'))["latitude"]), longitude=float(json.loads(data.get('location'))["longitude"]))
    await message.answer(_("Вы успешно создали круг\nПодтверждаете информацию если да то нажмите на галочку если нет то на крестик и вас перекинет к началу создания круга"), reply_markup=accept())
    await state.update_data(token=random_token)
    await state.set_state(CreateGroup.token)


@dp.message_handler(state=CreateGroup.token)
async def get_token(message: Message, state: FSMContext):
    if message.text == "❌":
        await message.answer(_("Главное меню"), reply_markup=menu())
        await state.set_state(UserRegistry.choose)
    else:
        data = await state.get_data()
        await DBCommands.create_group(user_id=message.from_user.id,
                                      name=data.get('name'),
                                      members=int(data.get('members')),
                                      money=data.get('money'),
                                      location=data.get('location'),
                                      start_date=data.get('start'),
                                      period=int(data.get('period')),
                                      link=data.get('link'),
                                      private=data.get('private'),
                                      token=data.get('token')
                                      )
        group = await DBCommands.search_group(data.get('token'))
        await DBCommands.update_user_in_group_id(user_id=message.from_user.id, group_id=group.id)
        await DBCommands.add_member(member=message.from_user.id, group_id=group.id, id_queue=1)
        await message.answer(_("Это ваш токен для приглашения,отправьте его друзьям чтобы они смогли присоедениться к вашему кругу: \n(Токен отдельным сообщением)"))
        await message.answer(data.get('token'), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.start, text=_("Старт"))
async def start_func(message: Message, state: FSMContext):
    await state.reset_state()
    try:
        group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
        group = await DBCommands.get_group_from_id(group_id=group_id)
        for user in await DBCommands.get_users_id_from_group_id(group_id=group_id, user_id=message.from_user.id):
            await bot.send_message(chat_id=user, text=_("Создатель круга") + group.name + _("стартовал"))
        if group.start != 1:
            await DBCommands.start_button(group_id)
            await message.answer(_("Поздравляем, вы завершили создание круга!\nПроверьте и подтвердите достоверность введеной вами информации, нажатием галочки. Если же вы хотите исправить какую нибудь информацию, то нажмите на крестик и бот перекинет вас к началу создания круга.") + group.start_date, reply_markup=menu_for_create_without_start())
            await state.set_state(CreateGroup.choose)

    except Exception as ex:
        await message.answer(_("Что-то пошло не так: ") + str(ex))


@dp.message_handler(state=CreateGroup.list_members, text=_("Список участников"))
async def list_members_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    if not users:
        await message.answer(_("Нет участинков"))
        await state.set_state(CreateGroup.choose)
    else:
        receiver = await DBCommands.get_queue_first(group_id=group_id)
        result = await DBCommands.get_confirmation(group_id=group_id, start_date=group.start_date)
        text = "Получатель: " + result['receiver'] + "\n"
        text += "Отправители     Статус\n"
        for i, j in zip(result['names'], result['accepts']):
            text += i + "    " + j + "\n"
        if receiver.member == message.from_user.id or group.start != 1:
            if len(users) % 2 == 0:
                for i in range(0, len(users), 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(_("⬅️Назад")))
            else:
                for i in range(0, len(users) - 1, 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_("⬅️Назад")))
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(CreateGroup.list_members_to)
        else:
            await message.answer(text)
            await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.list_members_to)
async def list_members_func_to(message: Message, state: FSMContext):
    receiver = await DBCommands.get_queue_first(await DBCommands.select_user_in_group_id(message.from_user.id))
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    to_user = await DBCommands.get_user_with_name(message.text)
    from_user = await DBCommands.get_user(message.from_user.id)
    user_queue = await DBCommands.get_user_from_table_member(user_id=message.from_user.id, group_id=group.id)
    if message.text == _("⬅️Назад"):
        if group.start == 0:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    elif receiver.member == message.from_user.id:
        await state.update_data(status_user=to_user.user_id, group_id=group.id, date=group.start_date, user_name=to_user.name)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("✅"), KeyboardButton("❌"))
        await message.answer(_("Сделал ли он платеж?"), reply_markup=keyboard)
        await state.set_state(CreateGroup.list_members_save)
    else:
        button_yes = InlineKeyboardButton(_("Да"), callback_data=str({"text": "yes",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        button_no = InlineKeyboardButton(_("Нет"), callback_data=str({"text": "no",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        keyboard = InlineKeyboardMarkup().add(button_yes, button_no)
        await bot.send_message(chat_id=to_user.user_id,
                               text=from_user.name + _("хочет поменяться его очередь ") + str(user_queue.id_queue),
                               reply_markup=keyboard)
        await message.answer(_("Ваш запрос ушел, ждем ответа"))


@dp.message_handler(state=CreateGroup.list_members_save)
async def list_members_func_save(message: Message, state: FSMContext):
    data = await state.get_data()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    users_id = await DBCommands.get_users_id_from_group_id(group_id=group_id, user_id=message.from_user.id)
    if len(users) % 2 == 0:
        for i in range(0, len(users), 2):
            keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
        keyboard.add(KeyboardButton(_("⬅️Назад")))
    else:
        for i in range(0, len(users) - 1, 2):
            keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
        keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_("⬅️Назад")))
    if message.text == "✅":
        await DBCommands.update_status(user_id=data['status_user'], group_id=data['group_id'], date=data['date'], status=1)
        await message.answer(_("Вы подтвердили платеж"), reply_markup=keyboard)
        for id in users_id:
            if id is not message.from_user.id:
                await bot.send_message(chat_id=id, text=f"Получатель подтвердил платеж от {data['user_name']}")
    elif message.text == "❌":
        await DBCommands.update_status(user_id=data['status_user'], group_id=data['group_id'], date=data['date'], status=0)
        await message.answer(_("Вы отменили платеж"), reply_markup=keyboard)
    await state.set_state(CreateGroup.list_members_to)


@dp.message_handler(state=CreateGroup.info, text=_("Общая информация"))
async def info_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    status = _("Закрытый") if group.private == 1 else _("Открытый")
    await message.answer("Имя круга: " + group.name + "\n" +
                         "Число участников: " + str(group.number_of_members) + "\n" +
                         "Сумма: " + group.amount + "\n" +
                         "Дата встречи: " + group.start_date + "\n" +
                         "Переодичность: " + str(group.period) + "\n" +
                         "Линк: " + group.link + "\n" +
                         "Приватность: " + status + "\n" +
                         "Токен: " + group.token + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(group.location)['latitude']), longitude=float(json.loads(group.location)['longitude']))
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.settings, text=_("Настройки"))
async def settings_func(message: Message, state: FSMContext):
    await state.reset_state()
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    await state.update_data(group_id=group.id)
    status = _("Закрытый") if group.private == 1 else _("Открытый")
    await message.answer(
        "Имя круга: " + group.name + "\n" +
        "Число участников: " + str(group.number_of_members) + "\n" +
        "Сумма: " + group.amount + "\n" +
        "Дата встречи: " + group.start_date + "\n" +
        "Переодичность: " + str(group.period) + "\n" +
        "Линк: " + group.link + "\n" +
        "Приватность: " + status + "\n" +
        "Локация: ", reply_markup=setting()
    )
    await message.answer_location(
        latitude=float(json.loads(group.location)['latitude']),
        longitude=float(json.loads(group.location)['longitude'])
    )
    await state.set_state(CreateGroup.settings_to)


@dp.message_handler(state=CreateGroup.settings_to)
async def settings_fun_to(message: Message, state: FSMContext):
    mapping = {
        _("Изменить имя"): ("name", "Введите имя"),
        _("Изменить дату встречи"): ("start_date", "Введите дату встречи дд/мм/гггг"),
        _("Изменить переодичность"): ("period", "Введите период"),
        _("Изменить линк"): ("link", "Введите линк"),
        _("Изменить локацию"): ("location", "Отправьте локацию"),
        _("Изменить язык"): ("language", "Изменить язык"),
        "⬅️Назад": (None, _("Главное меню"))
    }

    setting_data = mapping.get(message.text)
    if setting_data:
        setting, prompt = setting_data
        await state.update_data(setting=setting)
        if setting == 'language':
            await message.answer(prompt, reply_markup=get_language_keyboard())
            await state.set_state(CreateGroup.settings_save)
        elif setting:
            await message.answer(prompt)
            await state.set_state(CreateGroup.settings_save)
        else:
            group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
            if group.start == 0:
                await message.answer(_("Главное меню"), reply_markup=menu_for_create())
            else:
                await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
            await state.set_state(CreateGroup.choose)
    else:
        await message.answer(_("Выберите одну из кнопок"))
        await state.set_state(CreateGroup.settings_to)


@dp.message_handler(state=CreateGroup.settings_save, content_types=ContentType.ANY)
async def settings_fun_save(message: Message, state: FSMContext):
    data = await state.get_data()
    data_setting = data.get("setting")
    setting_value = json.dumps({'latitude': message.location.latitude, 'longitude': message.location.longitude}) \
        if data_setting == "location" and message.location else message.text
    if data_setting == "start_date" and not re.match(r'\d{2}/\d{2}/\d{4}', setting_value):
        await message.answer("Вы ввели неверную дату")
    elif data_setting == "location" and not message.location:
        await message.answer("Вы ввели неверно локацию")
    else:
        if message.text in LANGUAGES:
            await DBCommands.language_update(message.from_user.id, LANGUAGES[message.text])
            await message.answer("Успешно изменено", reply_markup=setting())
        elif await DBCommands.settings_update(data.get("group_id"), data_setting, setting_value):
            await message.answer("Успешно изменено")
        else:
            await message.answer("Не получилось изменить")
    await state.set_state(CreateGroup.settings_to)


@dp.message_handler(state=CreateGroup.complain, text=_("Пожаловаться"))
async def complain_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    if not users:
        await message.answer(_("Нет участинков"))
        await state.set_state(CreateGroup.choose)
    else:
        if len(users) % 2 == 0:
            for i in range(0, len(users), 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i+1]))
            keyboard.add(KeyboardButton(_("⬅️Назад")))
        else:
            for i in range(0, len(users) - 1, 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_("⬅️Назад")))
        await message.answer(_("Участники вашего круга"), reply_markup=keyboard)
        await state.set_state(CreateGroup.complain_to)


@dp.message_handler(state=CreateGroup.complain_to)
async def complain_to_func(message: Message, state: FSMContext):
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    if message.text == _("⬅️Назад"):
        if group.start == 0:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    else:
        await DBCommands.do_complain(message.text, group_id=group.id)
        await message.answer(_("Ваша жалоба принята"))
        await state.set_state(CreateGroup.complain_to)


@dp.message_handler(state=CreateGroup.my_group, text=_("Мои круги"))
async def my_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group_names = await DBCommands.select_all_groups(message.from_user.id, group_id)
    groups_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if group_names:
        for names in group_names:
            groups_keyboard.add(KeyboardButton(names))
        groups_keyboard.add(_("⬅️Назад"))
        await message.answer(_("Мои круги"), reply_markup=groups_keyboard)
        await state.set_state(CreateGroup.my_group_to)
    else:
        await message.answer(_("У вас только 1 круг"))
        await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.my_group_to)
async def my_group_func_to(message: Message, state: FSMContext):
    group_by_name = await DBCommands.search_group_by_name(message.text)
    if group_by_name:
        await DBCommands.update_user_in_group_id(message.from_user.id, group_by_name.id)
    group_ = await DBCommands.select_user_in_group_id(user_id=message.from_user.id)
    group_id = group_by_name.id if group_by_name else group_
    group = await DBCommands.get_group_from_id(group_id)
    if await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group_id) is True:
        if group.start == 0:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    else:
        await message.answer(_("Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=CreateGroup.choose_group, text=_("Выбор круга"))
async def choose_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_("Главное меню"), reply_markup=menu().add(KeyboardButton(_("⬅️Назад"))))
    await state.set_state(UserRegistry.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.choose)
async def choose_create(message: Message, state: FSMContext):
    if message.text in actions_create:
        action, new_state = actions_create[message.text]
        await action(message, state)
    else:
        await message.answer(_("Выберите одну из кнопок"))


actions_create = {
    _("Старт"): (start_func, CreateGroup.start),
    _("Список участников"): (list_members_func, CreateGroup.list_members),
    _("Общая информация"): (info_func, CreateGroup.info),
    _("Настройки"): (settings_func, CreateGroup.settings),
    _("Пожаловаться"): (complain_func, CreateGroup.complain),
    _("Выбор круга"): (choose_group_func, CreateGroup.choose_group),
    _("Мои круги"): (my_group_func, CreateGroup.my_group)
}


@dp.message_handler(text=_("⬅️Назад"), state="*")
async def back_function_create(message: Message, state: FSMContext):
    await state.reset_state()
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    if group.start == 0:
        await message.answer(_("Главное меню"), reply_markup=menu_for_create())
    else:
        await message.answer(_("Главное меню"), reply_markup=menu_for_create_without_start())
    await state.set_state(CreateGroup.choose)


