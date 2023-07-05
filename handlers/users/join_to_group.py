import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.menu import menu_for_join, menu, menu_for_create
from loader import dp, _
from states.states import JoinToGroup, UserRegistry
from text import main_menu, list_members, info, settings, complain, choose_gap, my_gap, choose_from_button, join_back
from utils.db_api.db_commands import DBCommands


@dp.message_handler(text=_(join_back), state="*")
async def back_function_join(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_(main_menu), reply_markup=menu_for_join())
    await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.join)
async def join_group(message: Message, state: FSMContext):
    gap = await DBCommands.search_group(message.text)
    queue = await DBCommands.get_queue(gap_id=gap.id)
    add_mem = await DBCommands.add_member(member=message.from_user.id, gap_id=gap.id, id_queue=queue.id_queue + 1)
    if gap is not None:
        if add_mem is True:
            await DBCommands.update_user_in_gap_id(message.from_user.id, gap_id=gap.id)
            await message.answer("Вы вошли в круг", reply_markup=menu_for_join())
            await state.set_state(JoinToGroup.choose)
        else:
            await message.answer("Количесвто учвстников ограничено")
    else:
        await message.answer("Нет такого круга", reply_markup=menu())
        await state.set_state(UserRegistry.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=JoinToGroup.list_members, text=_(list_members))
async def join_list_members_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_gap_id(gap_id=gap_id, user_id=message.from_user.id)
    gap = await DBCommands.get_gap_from_id(gap_id)
    if gap.start is not 1:
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
    else:
        result = await DBCommands.get_confirmation(gap_id=gap_id, start_date=gap.start_date)
        text = "Получатель: " + result['receiver'] + "\n"
        text += "Отправители     Статус\n"
        for i, j in zip(result['names'], result['accepts']):
            text += i + "    " + j + "\n"
        await message.answer(text)
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.list_members_to)
async def list_members_func_to(message: Message, state: FSMContext):
    if message.text == _(join_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(JoinToGroup.choose)
    else:
        gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
        await DBCommands.do_complain(message.text, gap_id=gap_id)
        await message.answer("Ваша жалоба принята")
        await state.set_state(JoinToGroup.list_members)


@dp.message_handler(state=JoinToGroup.info, text=_(info))
async def join_info_func(message: Message, state: FSMContext):
    await state.reset_state()
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    gap = await DBCommands.get_gap_from_id(gap_id)
    status = "Закрытый" if gap.private == 0 else "Открытый"
    await message.answer("Имя круга: " + gap.name + "\n" +
                         "Число участников: " + str(gap.number_of_members) + "\n" +
                         "Сумма: " + gap.amount + "\n" +
                         "Дата начала: " + gap.start_date + "\n" +
                         "Переодичность: " + str(gap.period) + "\n" +
                         "Линк: " + gap.link + "\n" +
                         "Приватность: " + status + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(gap.location)['latitude']), longitude=float(json.loads(gap.location)['longitude']))
    await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.complain, text=_(complain))
async def join_complain_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_gap_id(gap_id=gap_id, user_id=message.from_user.id)
    if not users:
        await message.answer("Нет участинков")
        await state.set_state(JoinToGroup.choose)
    else:
        if len(users) % 2 == 0:
            for i in range(0, len(users), 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i+1]))
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
        gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
        await DBCommands.do_complain(message.text, gap_id=gap_id)
        await message.answer("Ваша жалоба принята")
        await state.set_state(JoinToGroup.complain)


@dp.message_handler(state=JoinToGroup.my_gap, text=_(my_gap))
async def join_my_gap_func(message: Message, state: FSMContext):
    await state.reset_state()
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    gap_names = await DBCommands.select_all_gaps(message.from_user.id, gap_id)
    gaps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if gap_names is not []:
        for names in gap_names:
            gaps_keyboard.add(KeyboardButton(names))
        gaps_keyboard.add(_(join_back))
        await message.answer("my_gap", reply_markup=gaps_keyboard)
        await state.set_state(JoinToGroup.my_gap_to)
    else:
        await message.answer("У вас только 1 группа")


@dp.message_handler(state=JoinToGroup.my_gap_to)
async def my_gap_func_to(message: Message, state: FSMContext):
    await state.reset_state()
    gap = await DBCommands.search_group_by_name(message.text)
    await DBCommands.update_user_in_gap_id(message.from_user.id, gap.id)
    if await DBCommands.get_gap_now(user_id=message.from_user.id, gap_id=gap.id) is True:
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(JoinToGroup.choose)
    else:
        await message.answer(_(main_menu), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=JoinToGroup.choose_gap, text=_(choose_gap))
async def join_choose_gap_func(message: Message, state: FSMContext):
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
    _(choose_gap): (join_choose_gap_func, JoinToGroup.choose_gap),
    _(my_gap): (join_my_gap_func, JoinToGroup.my_gap)
}
