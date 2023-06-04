from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default.menu import menu_for_join
from loader import dp
from states.states import CreateGroup, JoinToGroup


@dp.message_handler(state=JoinToGroup.join)
async def join_group(message: Message, state: FSMContext):
    if message.text == "a":
        await message.answer("Вы вошли в круг", reply_markup=menu_for_join())
        await state.set_state(JoinToGroup.menu)
    else:
        await message.answer("Нет такого круга")
        await state.set_state(JoinToGroup.join)


@dp.message_handler(state=JoinToGroup.menu)
async def menu(message: Message, state: FSMContext):
    await message.answer("sansara")