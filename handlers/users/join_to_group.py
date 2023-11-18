import json
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default.menu import menu_for_join, menu, menu_for_create, menu_for_create_without_start, join_choose
from loader import dp, _, bot
from states.states import JoinToGroup, UserRegistry, CreateGroup
from utils.db_api.db_commands import DBCommands


@dp.message_handler(state=JoinToGroup.join)
async def join_group(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text in ["Назад ⬅️", "Orqaga ⬅️"]:
        group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
        if not group:
            await message.answer(_("📱Главное меню"), reply_markup=menu())
        elif group.user_id == message.from_user.id:
            await message.answer(_("📱Главное меню"), reply_markup=menu().add(KeyboardButton(_("⬅️Назад"))))
        else:
            await message.answer(_("📱Главное меню"), reply_markup=menu().add(KeyboardButton(_("⬅️ Назад"))))
        await state.set_state(UserRegistry.choose)
    elif message.text in ["➡️Войти по токену", "➡️Token bilan kiring"]:
        await message.answer(_("✍️Введите токен"))
        await state.set_state(JoinToGroup.join_token)
    elif message.text in ["👤Войти в открытые круги", "👤Ochiq doiralarga kirish"]:
        groups = await DBCommands.get_all_open_groups(user_id=message.from_user.id)
        if groups:
            for group in groups:
                keyboard.add(group)
            keyboard.add(_("Назад⬅️"))
            await message.answer(_("🔍Выберите открытые круги"), reply_markup=keyboard)
            await state.set_state(JoinToGroup.join_open)
        else:
            await message.answer(_("⚠️Нет открытых кругов"))
            await state.set_state(JoinToGroup.join)
    else:
        await message.answer(_("❇️Выберите одну из кнопок"))
        await state.set_state(JoinToGroup.join)


@dp.message_handler(state=JoinToGroup.join_token)
async def join_token(message: Message, state: FSMContext):
    try:
        group = await DBCommands.search_group(message.text)
        queue = await DBCommands.get_queue_last(group_id=group.id)
        add_mem = await DBCommands.add_member(member=message.from_user.id, group_id=group.id, id_queue=queue.id_queue + 1)
        if group is not None:
            if add_mem is True:
                await DBCommands.update_user_in_group_id(message.from_user.id, group_id=group.id)
                await message.answer(_("⚠️Вы вошли в круг"), reply_markup=menu_for_join())
                await message.answer(_("""⚠️Подсказка по кнопкам ниже:
📜Список участников- тут список участников круга с их статусом по оплатам. Также тут можно поменяться местами на получение денег с другими участниками. Если вы "Получатель Вознаграждения", то тут, вы можете отметить тех кто внес оплату.
📋Общая информация- тут вся информация о вашем круге. Если вы создатель круга,то тут вы можете поменять дату и место встречи и т.д. 
🆘Пожаловаться- тут вы можете пожаловаться на участников, которые нарушают условия участия. 🔍Выбор круга-тут вы можете вступить в другие круги. 
👥Мои круги-тут находятся ваши круги и тут вы можете перейти в них."""))
                await state.set_state(JoinToGroup.choose)
            else:
                await message.answer(_("🛑Количество участников ограничено"))
    except Exception as ex:
        logging.error(_("Что-то пошло не так: ") + str(ex))
        await message.answer(_("⚠️Нет такого круга"), reply_markup=join_choose())
        await state.set_state(JoinToGroup.join)


@dp.message_handler(state=JoinToGroup.join_open)
async def join_open(message: Message, state: FSMContext):
    if message.text in ["Назад⬅️", "Orqaga⬅️"]:
        await message.answer(_("👤Выберите в какой круг присоединиться"), reply_markup=join_choose())
        await state.set_state(JoinToGroup.join)
    else:
        try:
            group = await DBCommands.search_group_by_name(message.text)
            queue = await DBCommands.get_queue_last(group_id=group.id)
            add_mem = await DBCommands.add_member(member=message.from_user.id, group_id=group.id, id_queue=queue.id_queue + 1)
            if group is not None:
                if add_mem is True:
                    await DBCommands.update_user_in_group_id(message.from_user.id, group_id=group.id)
                    await message.answer(_("⚠️Вы вошли в круг"), reply_markup=menu_for_join())
                    await state.set_state(JoinToGroup.choose)
                else:
                    await message.answer(_("🛑Количество участников ограничено"))
        except Exception as ex:
            logging.error(_("Что-то пошло не так: ") + str(ex))
            await message.answer(_("⚠️Нет такого круга"), reply_markup=join_choose())
            await state.set_state(JoinToGroup.join)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=JoinToGroup.list_members, text=_("📜Список участников"))
async def join_list_members_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    if not users:
        await message.answer(_("🛑Нет участников"))
        await state.set_state(JoinToGroup.choose)
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
                keyboard.add(KeyboardButton(_("⬅️ Назад")))
            else:
                for i in range(0, len(users) - 1, 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_("⬅️ Назад")))
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(JoinToGroup.list_members_to)
        else:
            await message.answer(text)
            await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.list_members_to)
async def list_members_func_to(message: Message, state: FSMContext):
    receiver = await DBCommands.get_queue_first(await DBCommands.select_user_in_group_id(message.from_user.id))
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    to_user = await DBCommands.get_user_with_name(message.text)
    from_user = await DBCommands.get_user(message.from_user.id)
    user_queue = await DBCommands.get_user_from_table_member(user_id=message.from_user.id, group_id=group.id)
    if message.text in ["⬅️ Назад", "⬅️ Orqaga"]:
        await message.answer(_("📱Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    elif receiver.member == message.from_user.id:
        await state.update_data(status_user=to_user.user_id, group_id=group.id, date=group.start_date, user_name=to_user.name)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("✅"), KeyboardButton("❌"))
        await message.answer(_("⚠️Сделал ли он платеж?"), reply_markup=keyboard)
        await state.set_state(JoinToGroup.list_members_save)
    else:
        button_yes = InlineKeyboardButton(_("Да"), callback_data=str({"text": "yes",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        button_no = InlineKeyboardButton(_("Нет"), callback_data=str({"text": "no",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        keyboard = InlineKeyboardMarkup().add(button_yes, button_no)
        await bot.send_message(chat_id=to_user.user_id,
                               text="⚠️" + from_user.name + _(" 🔄 хочет поменяться с вами очередями на получение вознаграждения, хотите ли вы поменяться?\nЕго очередь: ") + str(user_queue.id_queue),
                               reply_markup=keyboard)
        await message.answer(_("⚠️Ваш запрос отправлен, ожидайте ответа"))


@dp.message_handler(state=JoinToGroup.list_members_save)
async def list_members_func_save(message: Message, state: FSMContext):
    data = await state.get_data()
    users_id = await DBCommands.get_users_id_from_group_id(group_id=data['group_id'], user_id=message.from_user.id)
    if message.text == "✅":
        await DBCommands.update_status(user_id=data['status_user'], group_id=data['group_id'], date=data['date'], status=1)
        await message.answer(_("⚠️Вы подтвердили платеж"))
        for id in users_id:
            if id is not message.from_user.id:
                await bot.send_message(chat_id=id, text=f"Получатель подтвердил платеж от {data['user_name']}")
    if message.text == "❌":
        await DBCommands.update_status(user_id=data['status_user'], group_id=data['group_id'], date=data['date'], status=1)
        await message.answer(_("🛑Вы отменили платеж"))
    await state.set_state(JoinToGroup.list_members)


@dp.message_handler(state=JoinToGroup.info, text=_("📋Общая информация"))
async def join_info_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    recieve = await DBCommands.get_member_recieve(group_id=group_id, date=group.start_date)
    status = _("🔒Закрытый") if group.private == 1 else _("🔓Открытый")
    await message.answer("Имя круга: " + group.name + "\n" +
                         "Число участников: " + str(group.number_of_members) + "\n" +
                         "Имя получателя: " + str(recieve.name) + "\n" +
                         "Сумма: " + group.amount + "\n" +
                         "Дата начала: " + group.start_date + "\n" +
                         "Периодичность: " + str(group.period) + "\n" +
                         "Линк: " + group.link + "\n" +
                         "Приватность: " + status + "\n" +
                         "Токен: " + group.token + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(group.location)['latitude']),
                                  longitude=float(json.loads(group.location)['longitude']))
    await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.complain, text=_("🆘Пожаловаться"))
async def join_complain_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    if not users:
        await message.answer(_("🛑Нет участников"))
        await state.set_state(JoinToGroup.choose)
    else:
        if len(users) % 2 == 0:
            for i in range(0, len(users), 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(_("⬅️ Назад")))
        else:
            for i in range(0, len(users) - 1, 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_("⬅️ Назад")))
        await message.answer(_("👥Участники вашего круга"), reply_markup=keyboard)
        await state.set_state(JoinToGroup.complain_to)


@dp.message_handler(state=JoinToGroup.complain_to)
async def join_complain_to_func(message: Message, state: FSMContext):
    if message.text in ["⬅️ Назад", "⬅️ Orqaga"]:
        await message.answer(_("📱Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)
    else:
        group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
        user = await DBCommands.do_complain(message.text, group_id=group_id)
        await message.answer(_("⚠️Ваша жалоба принята"))
        await bot.send_message(user.user_id, "⚠️ " + user.name + _(" пожаловался на вас, если вы с этим не согласны, напишите в тех.поддержку."))
        await state.set_state(JoinToGroup.complain)


@dp.message_handler(state=JoinToGroup.my_group, text=_("👥Мои круги"))
async def join_my_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group_names = await DBCommands.select_all_groups(message.from_user.id, group_id)
    groups_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if group_names:
        for names in group_names:
            groups_keyboard.add(KeyboardButton(names))
        groups_keyboard.add(_("⬅️ Назад"))
        await message.answer(_("👥Мои круги"), reply_markup=groups_keyboard)
        await state.set_state(JoinToGroup.my_group_to)
    else:
        await message.answer(_("⚠️У вас только 1 круг"))
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.my_group_to)
async def my_group_func_to(message: Message, state: FSMContext):
    group_by_name = await DBCommands.search_group_by_name(message.text)
    if group_by_name:
        await DBCommands.update_user_in_group_id(message.from_user.id, group_by_name.id)
    group_ = await DBCommands.select_user_in_group_id(user_id=message.from_user.id)
    group_id = group_by_name.id if group_by_name else group_
    group = await DBCommands.get_group_from_id(group_id)
    if await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group_id) is True:
        if group.start == 0:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create())
        else:
            await message.answer(_("📱Главное меню"), reply_markup=menu_for_create_without_start())
        await state.set_state(CreateGroup.choose)
    else:
        await message.answer(_("📱Главное меню"), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.choose_group, text=_("🔍Выбор круга"))
async def join_choose_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_("❇️Выберите одну из кнопок:"), reply_markup=menu().add(KeyboardButton(_("⬅️ Назад"))))
    await state.set_state(UserRegistry.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=JoinToGroup.choose)
async def choose_join(message: Message, state: FSMContext):
    if message.text in actions_join:
        action, new_state = actions_join[message.text]
        await action(message, state)
    else:
        await message.answer(_("❇️Выберите одну из кнопок"), reply_markup=menu_for_join())


actions_join = {
    _("📜Список участников"): (join_list_members_func, JoinToGroup.list_members),
    _("📋Общая информация"): (join_info_func, JoinToGroup.info),
    _("🆘Пожаловаться"): (join_complain_func, JoinToGroup.complain),
    _("🔍Выбор круга"): (join_choose_group_func, JoinToGroup.choose_group),
    _("👥Мои круги"): (join_my_group_func, JoinToGroup.my_group),

    _("📜Davrangiz a'zolari"): (join_list_members_func, JoinToGroup.list_members),
    _("📋Umumiy ma'lumot"): (join_info_func, JoinToGroup.info),
    _("🆘Shikoyat"): (join_complain_func, JoinToGroup.complain),
    _("🔍Davra tanlash"): (join_choose_group_func, JoinToGroup.choose_group),
    _("👥Mening davralarim"): (join_my_group_func, JoinToGroup.my_group)
}
