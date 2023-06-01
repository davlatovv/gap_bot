from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default.menu import money, period
from loader import dp
from states.states import CreateGroup
from text import create_group


@dp.message_handler(text=create_group)
async def create_group(message: Message, state: FSMContext):
    await message.answer("Выберите сумму", reply_markup=money())
    await state.set_state(CreateGroup.period)


@dp.message_handler(state=CreateGroup.money)
async def choose_period(message: Message, state: FSMContext):
    await state.set_state(CreateGroup.create)
    await message.answer("Выберите переодичность", reply_markup=period())
