import json
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType, ReplyKeyboardRemove

from keyboards.default.menu import money, period, accept, menu_for_create, location, private, menu, back_state, \
    menu_for_join
from loader import dp, random_token, _
from states.states import CreateGroup, UserRegistry, JoinToGroup
from text import create_back, your_token, check_info, my_gap, start, list_members, \
    info, complain, choose_gap, settings, choose_from_button, send_money, send_members, send_name, send_location, \
    send_link, send_start, send_period, send_private, onse_week, digit, onse_month, accept_registration, create_group, \
    join_group, main_menu, public, privates, no, invalid_date_format
from utils.db_api.db_commands import DBCommands


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REGISTRATION GAP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.name)
async def choose_name(message: Message, state: FSMContext):
    await message.answer(_(send_name), reply_markup=back_state())
    await state.set_state(CreateGroup.money)


@dp.message_handler(text=_(create_back), state=CreateGroup.money)
async def go_back_to_name(message: Message, state: FSMContext):
    await message.answer(_(main_menu), reply_markup=menu())
    await state.set_state(UserRegistry.choose)


@dp.message_handler(state=CreateGroup.money)
async def choose_money(message: Message, state: FSMContext):
    await message.answer(_(send_money), reply_markup=money())
    await state.update_data(name=message.text)
    await state.set_state(CreateGroup.members)


@dp.message_handler(text=_(create_back), state=CreateGroup.members)
async def go_back_to_money(message: Message, state: FSMContext):
    await message.answer(_(send_name), reply_markup=back_state())
    await state.set_state(CreateGroup.money)


@dp.message_handler(state=CreateGroup.members)
async def choose_money(message: Message, state: FSMContext):
    await message.answer(_(send_members), reply_markup=back_state())
    await state.update_data(money=message.text)
    await state.set_state(CreateGroup.location)


@dp.message_handler(text=_(create_back), state=CreateGroup.location)
async def go_back_to_members(message: Message, state: FSMContext):
    await message.answer(_(send_money), reply_markup=money())
    await state.set_state(CreateGroup.members)


@dp.message_handler(state=CreateGroup.location)
async def choose_members(message: Message, state: FSMContext):
    await message.answer(_(send_location), reply_markup=location())
    if message.text.isdigit():
        await state.update_data(members=message.text)
    else:
        await message.answer(_(digit))
    await state.set_state(CreateGroup.link)


@dp.message_handler(text=_(create_back), state=CreateGroup.link)
async def go_back_to_location(message: Message, state: FSMContext):
    await message.answer(_(send_members), reply_markup=back_state())
    await state.set_state(CreateGroup.location)


@dp.message_handler(state=CreateGroup.link, content_types=ContentType.LOCATION)
async def choose_location(message: Message, state: FSMContext):
    await message.answer(_(send_link), reply_markup=back_state())
    await state.update_data(location=json.dumps({'latitude': message.location.latitude, 'longitude': message.location.longitude}))
    await state.set_state(CreateGroup.start)


@dp.message_handler(text=_(create_back), state=CreateGroup.start)
async def go_back_to_link(message: Message, state: FSMContext):
    await message.answer(_(send_location), reply_markup=location())
    await state.set_state(CreateGroup.link)


@dp.message_handler(state=CreateGroup.start)
async def choose_start(message: Message, state: FSMContext):
    await message.answer(_(send_start), reply_markup=back_state())
    await state.update_data(link=message.text)
    await state.set_state(CreateGroup.period)


@dp.message_handler(text=_(create_back), state=CreateGroup.period)
async def go_back_to_start(message: Message, state: FSMContext):
    await message.answer(_(send_link), reply_markup=back_state())
    await state.set_state(CreateGroup.start)


@dp.message_handler(state=CreateGroup.period)
async def choose_period(message: Message, state: FSMContext):
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    if re.match(date_pattern, message.text):
        await message.answer(_(send_period), reply_markup=period())
        await state.update_data(start=message.text)
        await state.set_state(CreateGroup.private)
    else:
        await message.answer(_(invalid_date_format))


@dp.message_handler(text=_(create_back), state=CreateGroup.private)
async def go_back_to_period(message: Message, state: FSMContext):
    await message.answer(_(send_start), reply_markup=back_state())
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.private)
async def choose_private(message: Message, state: FSMContext):
    if message.text == _(onse_week):
        await state.update_data(period=7)
    elif message.text == _(onse_month):
        await state.update_data(period=30)
    else:
        if message.text.isdigit():
            await state.update_data(period=message.text)
        else:
            await message.answer(_(digit))
    await message.answer(_(send_private), reply_markup=private())
    await state.set_state(CreateGroup.accept)


@dp.message_handler(text=_(create_back), state=CreateGroup.accept)
async def go_back_to_period(message: Message, state: FSMContext):
    await message.answer(_(send_period), reply_markup=period())
    await state.set_state(CreateGroup.private)


@dp.message_handler(state=CreateGroup.accept)
async def validation(message: Message, state: FSMContext):
    if message.text == public:
        await state.update_data(private=1)
    elif message.text == privates:
        await state.update_data(private=0)
    else:
        await message.answer(_(choose_from_button))
    data = await state.get_data()
    await message.answer("Имя круга: " + str(data.get('name')) + "\n" +
                         "Число участников: " + str(data.get('members')) + "\n" +
                         "Сумма: " + str(data.get('money')) + "\n" +
                         "Дата начала: " + str(data.get('start')) + "\n" +
                         "Переодичность: " + str(data.get('period')) + "\n" +
                         "Линк: " + str(data.get('link')) + "\n" +
                         "Приватность: " + str(data.get('private')) + "\n" +
                         "Локация: ")
    await message.answer_location(latitude=float(json.loads(data.get('location'))["latitude"]), longitude=float(json.loads(data.get('location'))["longitude"]))
    await message.answer(_(check_info), reply_markup=accept())
    await state.update_data(token=random_token)
    await state.set_state(CreateGroup.token)


@dp.message_handler(state=CreateGroup.token)
async def get_token(message: Message, state: FSMContext):
    if message.text == no:
        await message.answer(_(main_menu), reply_markup=menu())
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
        gap = await DBCommands.search_group(data.get('token'))
        await DBCommands.update_user_in_gap_id(user_id=message.from_user.id, gap_id=gap.id)
        await DBCommands.add_member(member=message.from_user.id, gap_id=gap.id, id_queue=1)
        await message.answer(_(your_token) + data.get('token'), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)


'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BRIDGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.choose)
async def choose_create(message: Message, state: FSMContext):
    if message.text in actions_create:
        action, new_state = actions_create[message.text]
        await action(message, state)
    else:
        await message.answer(_(choose_from_button))


@dp.message_handler(text=_(create_back), state="*")
async def back_function_create(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_(main_menu), reply_markup=menu_for_create())
    await state.set_state(CreateGroup.choose)

'''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MENU<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


@dp.message_handler(state=CreateGroup.start, text=_(start))
async def start_func(message: Message, state: FSMContext):
    await state.reset_state()
    try:
        gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
        gap = await DBCommands.get_gap_from_id(gap_id=gap_id)
        if gap.start is not 1:
            await DBCommands.start_button(gap_id)
            await message.answer("Вы успешно начали гап " + gap.start_date)
            await state.set_state(CreateGroup.choose)
        else:
            await message.answer("Вы уже стартовали гап")
            await state.set_state(CreateGroup.choose)
    except Exception as ex:
        await message.answer("Повторите" + str(ex))


@dp.message_handler(state=CreateGroup.list_members, text=_(list_members))
async def list_members_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_gap_id(gap_id=gap_id, user_id=message.from_user.id)
    gap = await DBCommands.get_gap_from_id(gap_id)
    if gap.start is not 1:
        if not users:
            await message.answer("Нет участинков")
            await state.set_state(CreateGroup.choose)
        else:
            if len(users) % 2 == 0:
                for i in range(0, len(users), 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i+1]))
                keyboard.add(KeyboardButton(_(create_back)))
            else:
                for i in range(0, len(users) - 1, 2):
                    keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
                keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_(create_back)))
            await message.answer("Участники", reply_markup=keyboard)
            await state.set_state(CreateGroup.complain_to)
    else:
        info = ""
        result = await DBCommands.get_confirmation(gap_id=gap_id, start_date=gap.start_date)
        info += "Получатель: " + result['receiver'] + "\n"
        info += "Отправители     Статус\n"
        for i, j in zip(result['names'], result['accepts']):
            info += i + "    " + j + "\n"
        await message.answer(info)
        await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.list_members_to)
async def list_members_func_to(message: Message, state: FSMContext):
    if message.text == _(create_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    else:
        gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
        await DBCommands.do_complain(message.text, gap_id=gap_id)
        await message.answer("Ваша жалоба принята")
        await state.set_state(CreateGroup.list_members)


@dp.message_handler(state=CreateGroup.info, text=_(info))
async def info_func(message: Message, state: FSMContext):
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
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.settings, text=_(settings))
async def settings_func(message: Message, state: FSMContext):
    await state.reset_state()
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    await message.answer("settings")
    await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.complain, text=_(complain))
async def complain_func(message: Message, state: FSMContext):
    await state.reset_state()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    users = await DBCommands.get_users_name_from_gap_id(gap_id=gap_id, user_id=message.from_user.id)
    if not users:
        await message.answer("Нет участинков")
        await state.set_state(CreateGroup.choose)
    else:
        if len(users) % 2 == 0:
            for i in range(0, len(users), 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i+1]))
            keyboard.add(KeyboardButton(_(create_back)))
        else:
            for i in range(0, len(users) - 1, 2):
                keyboard.add(KeyboardButton(users[i]), KeyboardButton(users[i + 1]))
            keyboard.add(KeyboardButton(users[-1]), KeyboardButton(_(create_back)))
        await message.answer("Участники", reply_markup=keyboard)
        await state.set_state(CreateGroup.complain_to)


@dp.message_handler(state=CreateGroup.complain_to)
async def complain_to_func(message: Message, state: FSMContext):
    if message.text == _(create_back):
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    else:
        gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
        await DBCommands.do_complain(message.text, gap_id=gap_id)
        await message.answer("Ваша жалоба принята")
        await state.set_state(CreateGroup.complain)


@dp.message_handler(state=CreateGroup.my_gap, text=_(my_gap))
async def my_gap_func(message: Message, state: FSMContext):
    await state.reset_state()
    gap_id = await DBCommands.select_user_in_gap_id(message.from_user.id)
    gap_names = await DBCommands.select_all_gaps(message.from_user.id, gap_id)
    gaps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if gap_names:
        for names in gap_names:
            gaps_keyboard.add(KeyboardButton(names))
        gaps_keyboard.add(_(create_back))
        await message.answer("my_gap", reply_markup=gaps_keyboard)
        await state.set_state(CreateGroup.my_gap_to)
    else:
        await message.answer("У вас только 1 группа")
        await state.set_state(CreateGroup.choose)


@dp.message_handler(state=CreateGroup.my_gap_to)
async def my_gap_func_to(message: Message, state: FSMContext):
    await state.reset_state()
    gap = await DBCommands.search_group_by_name(message.text)
    await DBCommands.update_user_in_gap_id(message.from_user.id, gap.id)
    if await DBCommands.get_gap_now(user_id=message.from_user.id, gap_id=gap.id) is True:
        await message.answer(_(main_menu), reply_markup=menu_for_create())
        await state.set_state(CreateGroup.choose)
    else:
        await message.answer(_(main_menu), reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.choose)


@dp.message_handler(state=CreateGroup.choose_gap, text=_(choose_gap))
async def choose_gap_func(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_(main_menu), reply_markup=menu().add(KeyboardButton(_(create_back))))
    await state.set_state(UserRegistry.choose)

actions_create = {
    _(start): (start_func, CreateGroup.start),
    _(list_members): (list_members_func, CreateGroup.list_members),
    _(info): (info_func, CreateGroup.info),
    _(settings): (settings_func, CreateGroup.settings),
    _(complain): (complain_func, CreateGroup.complain),
    _(choose_gap): (choose_gap_func, CreateGroup.choose_gap),
    _(my_gap): (my_gap_func, CreateGroup.my_gap)
}



