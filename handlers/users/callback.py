from aiogram.types import CallbackQuery
from aiogram.utils.json import json

from loader import dp, bot, _
from utils.db_api.db_commands import DBCommands


@dp.callback_query_handler(lambda callback_query: callback_query.data[10:13] == 'yes', state="*")
async def handle_yes_button(callback_query: CallbackQuery):
    data = eval(callback_query.data)
    from_user = data['from_user']
    group = data['group']
    if await DBCommands.change_queue(user_id_from=callback_query.from_user.id, user_id_to=from_user, group_id=group):
        user_queue = await DBCommands.get_user_from_member(group_id=group, user_id=callback_query.from_user.id)
        await bot.send_message(chat_id=int(callback_query.from_user.id), text=_("🔄Вы успешно поменялись, теперь ваша очередь ") + str(user_queue.id_queue))
        to_user_queue = await DBCommands.get_user_from_member(group_id=group, user_id=from_user)
        await bot.send_message(chat_id=int(from_user), text=_("🔄Вы успешно поменялись, теперь ваша очередь ") + str(to_user_queue.id_queue))
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    else:
        await callback_query.answer(_("⚠️Что-то пошло не так: "))
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda callback_query: callback_query.data[10:12] == 'no', state="*")
async def handle_no_button(callback_query: CallbackQuery):
    await callback_query.answer(_("🛑Вы нажали кнопку 'Нет'"))
    data = eval(callback_query.data)
    from_user = data['from_user']
    await bot.send_message(chat_id=int(from_user),
                           text=_("🛑Вам отказали"))
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


