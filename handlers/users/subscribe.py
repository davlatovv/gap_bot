from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import *

from data.config import PAYME_TOKEN
from keyboards.default.menu import menu_for_create, menu_for_create_without_start, menu_for_join
from loader import _, dp, bot
from states.states import Subscribe
from utils.db_api.db_commands import DBCommands


@dp.message_handler(state=Subscribe.subscribe, text=_("🎫ПОДПИСКА"))
async def cmd_pay(message: Message, state: FSMContext):
    user = await DBCommands.get_user(message.from_user.id)
    amount = 50000
    await state.update_data(amount=amount)
    if user.subscribe == 0:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title=_('Подписка'),
            description=_("Подписка"),
            payload='original',
            provider_token=PAYME_TOKEN,
            start_parameter='original',
            currency='UZS',
            prices=[
                LabeledPrice(label=_('Подписка'), amount=amount),
            ],
            photo_url="https://i.ibb.co/V9Kw68Q/photo-2023-02-18-16-52-46.jpg",
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False,
        )


@dp.message_handler(content_types=[ContentType.SUCCESSFUL_PAYMENT])
async def success_payment(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    amount = await state.get_data("amount")
    try:
        user = await DBCommands.get_user(message.from_user.id)
        new_date = (datetime.today() + timedelta(days=30)).strftime('%d-%m-%Y')
        await user.update(subscribe=1, end_date=new_date).apply()
        group = await DBCommands.get_group_from_id(await DBCommands.select_user_in_group_id(user_id=user.user_id))
        await DBCommands.creat_subscribe(user_id=user.user_id, amount=amount,
                                         start_date=datetime.today().strftime('%d-%m-%Y'), end_date=new_date)
        if group.user_id == user.user_id:
            if group.start == 0:
                await message.answer(_("🎉Поздравляю!\n✅Вы успешно приобрели подписку!\nТеперь пользоваться ботом будет еще приятнее🤑"), reply_markup=menu_for_create())
            else:
                await message.answer(_("🎉Поздравляю!\n✅Вы успешно приобрели подписку!\nТеперь пользоваться ботом будет еще приятнее🤑"), reply_markup=menu_for_create_without_start())
        else:
            await message.answer(_("🎉Поздравляю!\n✅Вы успешно приобрели подписку!\nТеперь пользоваться ботом будет еще приятнее🤑"), reply_markup=menu_for_join())
    except Exception as ex:
        await message.answer(_("Что то пошло не так, попробуйте позже") + ex, reply_markup=keyboard.add(_("🎫ПОДПИСКА")))
        await state.set_state(Subscribe.subscribe)


