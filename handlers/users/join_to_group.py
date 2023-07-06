import json
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default.menu import menu_for_join, menu, menu_for_create
from loader import dp, _, bot
from states.states import JoinToGroup, UserRegistry, CreateGroup
from text import *
from utils.db_api.db_commands import DBCommands


@dp.message_handler(text=_(join_back), state="*")
async def back_function_join(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_(main_menu), reply_markup=menu_for_join())
    await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.join)
async def join_group(message: Message, state: FSMContext):
    try:
        group = await DBCommands.search_group(message.text)
        queue = await DBCommands.get_queue(group_id=group.id)
        add_mem = await DBCommands.add_member(member=message.from_user.id, group_id=group.id, id_queue=queue.id_queue + 1)
        if group is not None:
            if add_mem is True:
                await DBCommands.update_user_in_group_id(message.from_user.id, group_id=group.id)
                await message.answer("Вы вошли в круг", reply_markup=menu_for_join())
                await state.set_state(JoinToGroup.choose)
            else:
                await message.answer("Количесвто учвстников ограничено")
    except Exception as ex:
        logging.error("Join to group error: " + str(ex))
        group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
        if group.user_id == message.from_user.id:
            await message.answer("Нет такого круга", reply_markup=menu().add(KeyboardButton(_(create_back))))
        else:
            await message.answer("Нет такого круга", reply_markup=menu().add(KeyboardButton(_(join_back))))
        await state.set_state(UserRegistry.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=JoinToGroup.list_members, text=_(list_members))
async def join_list_members_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    receiver = await DBCommands.get_queue(group_id=group_id)
    result = await DBCommands.get_confirmation(group_id=group_id, start_date=group.start_date)
    text = "Получатель: " + result['receiver'] + "\n"
    text += "Отправители     Статус\n"
    for i, j in zip(result['names'], result['accepts']):
        text += i + "    " + j + "\n"
    if group.start != 1 or receiver.member == message.from_user.id:
        if not users:
            await message.answer("Нет участинков")
            await state.set_state(JoinToGroup.choose)
        else:
            if len(users) % 2 == 0:
                for i in range(0, len(users), 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(_(join_back)))
            else:
                for i in range(0, len(users) - 1, 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_(join_back)))
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(JoinToGroup.list_members_to)
    else:
        await message.answer(text)
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.list_members_to)
async def list_members_func_to(message: Message, state: FSMContext):
    receiver = await DBCommands.get_queue(await DBCommands.select_user_in_group_id(message.from_user.id))
    group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(message.from_user.id))
    to_user = await DBCommands.get_user_with_name(message.text)
    from_user = await DBCommands.get_user(message.from_user.id)
    user_queue = await DBCommands.get_user_from_table_member(user_id=message.from_user.id, group_id=group.id)
    if message.text == _(join_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(JoinToGroup.choose)
    elif receiver.member == message.from_user.id:
        await state.update_data(status_user=to_user, group_id=group.id, date=group.start_date)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(yes), KeyboardButton(no))
        await message.answer("Сделал ли он оплату ?",reply_markup=keyboard)
        await state.set_state(JoinToGroup.list_members_save)
    else:
        button_yes = InlineKeyboardButton("Да", callback_data=str({"text": "yes",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        button_no = InlineKeyboardButton("Нет", callback_data=str({"text": "no",
                                                                   "from_user": from_user.user_id,
                                                                   "group": group.id}))
        keyboard = InlineKeyboardMarkup().add(button_yes, button_no)
        await bot.send_message(chat_id=to_user.user_id,
                               text=from_user.name + "хочет поменяться его очередь " + str(user_queue.id_queue), reply_markup=keyboard)
        await message.answer("Ваш запрос ушел, ждем ответа")


@dp.message_handler(state=JoinToGroup.list_members_save)
async def list_members_func_save(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == yes:
        await DBCommands.update_status(user_id=data['status_user'],group_id=data['group_id'], date=data['date'], status=1)
        await message.answer("Вы подтвердили платеж")
    if message.text == no:
        await DBCommands.update_status(user_id=data['status_user'], group_id=data['group_id'], date=data['date'], status=1)
        await message.answer("Вы отменили платеж")
    await state.set_state(JoinToGroup.list_members)


@dp.message_handler(state=JoinToGroup.info, text=_(info))
async def join_info_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group = await DBCommands.get_group_from_id(group_id)
    status = "Закрытый" if group.private == 0 else "Открытый"
    await message.answer("Имя круга: " + group.name + "\n" +
                         "Число участников: " + str(group.number_of_members) + "\n" +
                         "Сумма: " + group.amount + "\n" +
                         "Дата начала: " + group.start_date + "\n" +
                         "Переодичность: " + str(group.period) + "\n" +
                         "Линк: " + group.link + "\n" +
                         "Приватность: " + status + "\n" +
                         "Токен: " + group.token + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(group.location)['latitude']),
                                  longitude=float(json.loads(group.location)['longitude']))
    await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.complain, text=_(complain))
async def join_complain_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_group_id(group_id=group_id, user_id=message.from_user.id)
    if not users:
        await message.answer("Нет участинков")
        await state.set_state(JoinToGroup.choose)
    else:
        if len(users) % 2 == 0:
            for i in range(0, len(users), 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(_(join_back)))
        else:
            for i in range(0, len(users) - 1, 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_(join_back)))
        await message.answer("Участники", reply_markup=keyboard)
        await state.set_state(JoinToGroup.complain_to)


@dp.message_handler(state=JoinToGroup.complain_to)
async def join_complain_to_func(message: Message, state: FSMContext):
    if message.text == _(join_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(JoinToGroup.choose)
    else:
        group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
        await DBCommands.do_complain(message.text, group_id=group_id)
        await message.answer("Ваша жалоба принята")
        await state.set_state(JoinToGroup.complain)


@dp.message_handler(state=JoinToGroup.my_group, text=_(my_group))
async def join_my_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    group_id = await DBCommands.select_user_in_group_id(message.from_user.id)
    group_names = await DBCommands.select_all_groups(message.from_user.id, group_id)
    groups_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if group_names:
        for names in group_names:
            groups_keyboard.add(KeyboardButton(names))
        groups_keyboard.add(_(create_back))
        await message.answer("my_group", reply_markup=groups_keyboard)
        await state.set_state(JoinToGroup.my_group_to)
    else:
        await message.answer("У вас только 1 группа")
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.my_group_to)
async def my_group_func_to(message: Message, state: FSMContext):
    await state.reset_state()
    group = await DBCommands.search_group_by_name(message.text)
    await DBCommands.update_user_in_group_id(message.from_user.id, group.id)
    if await DBCommands.get_group_now(user_id=message.from_user.id, group_id=group.id) is True:
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    else:
        await message.answer(_(main_menu), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.choose_group, text=_(choose_group))
async def join_choose_group_func(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_(main_menu), reply_markup=menu().add(KeyboardButton(_(join_back))))
    await state.set_state(UserRegistry.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=JoinToGroup.choose)
async def choose_join(message: Message, state: FSMContext):
    if message.text in actions_join:
        action, new_state = actions_join[message.text]
        await action(message, state)
    else:
        await message.answer(_(choose_from_button))


actions_join = {
    _(list_members): (join_list_members_func, JoinToGroup.list_members),
    _(info): (join_info_func, JoinToGroup.info),
    _(complain): (join_complain_func, JoinToGroup.complain),
    _(choose_group): (join_choose_group_func, JoinToGroup.choose_group),
    _(my_group): (join_my_group_func, JoinToGroup.my_group)
}
