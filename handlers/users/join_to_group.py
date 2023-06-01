from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp
from states.states import CreateGroup, JoinToGroup

#
# @dp.message_handler(text='Создать круг', state=JoinToGroup.join)
# async def join_group(message: Message, state: FSMContext):