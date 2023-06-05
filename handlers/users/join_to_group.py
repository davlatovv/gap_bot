from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default.menu import menu_for_join
from loader import dp
from states.states import CreateGroup, JoinToGroup
from utils.db_api.db_commands import DBCommands


@dp.message_handler(state=JoinToGroup.join)
async def join_group(message: Message, state: FSMContext):
    if DBCommands.search_group(message.text):
        await DBCommands.add_member(message.from_user.id)
        await message.answer("Вы вошли в круг", reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.menu)
    else:
        await message.answer("Нет такого круга")
        await state.set_state(JoinToGroup.join)


@dp.message_handler(state=JoinToGroup.menu)
async def menu(message: Message, state: FSMContext):
    await message.answer("sansara")