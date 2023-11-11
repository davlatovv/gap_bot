from datetime import datetime, timedelta
from typing import List
from states.states import Subscribe
from .models import *


class DBCommands:
    @staticmethod
    async def process_groups():
        today = datetime.today().strftime('%d/%m/%Y')
        groups = await Group.query.gino.all()

        for group in groups:
            queue_members = await DBCommands.queue(group_id=group.id)

            if group.start_date == today:
                new_date = (datetime.today() + timedelta(days=group.period)).strftime('%d/%m/%Y')
                await group.update(start_date=new_date).apply()

                for i, member in enumerate(queue_members):
                    if i == 0:
                        update_id = await Member.query.where(
                            and_(Member.group_id == group.id, Member.member == member)).gino.first()
                        last_id = await Member.query.where(
                            and_(Member.group_id == group.id, Member.member == queue_members[-1])).gino.first()
                        await update_id.update(id_queue=last_id.id_queue).apply()
                    else:
                        confirm = Confirmation(group_id=group.id, member_recieve=queue_members[0], member_get=member,
                                               date=new_date, accept=0)
                        await confirm.create()

                        update_id = await Member.query.where(
                            and_(Member.group_id == group.id, Member.member == member)).gino.first()
                        await update_id.update(id_queue=update_id.id_queue - 1).apply()

    @staticmethod
    async def process_subscribe():
        from aiogram.dispatcher import FSMContext
        from aiogram.types import ReplyKeyboardMarkup
        from loader import bot, _
        today = datetime.today().strftime('%d-%m-%Y')
        users = await User.query.where(and_(User.subscribe == 1, User.end_date == today)).gino.all()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for user in users:
            await user.update(subscribe=0).apply()
            await bot.send_message(chat_id=user.user_id, text=_("⚠️Ваше время истекло, теперь приобретите подписку"), reply_markup=keyboard.add(_("ПОДПИСКА")))
            await FSMContext.set_state(Subscribe.subscribe)

    @staticmethod
    async def creat_subscribe(user_id,
                          amount,
                          start_date,
                          end_date,):
        subscribe = SubscribeUsers(user_id=user_id, amount=amount, start_date=start_date, end_date=end_date)
        await subscribe.create()
        return subscribe

    @staticmethod
    async def get_queue_first(group_id: int):
        queue = await Member.query.where(Member.group_id == group_id).order_by(asc(Member.id_queue)).gino.first()
        return queue

    @staticmethod
    async def get_queue_last(group_id: int):
        queue = await Member.query.where(Member.group_id == group_id).order_by(desc(Member.id_queue)).gino.first()
        return queue

    @staticmethod
    async def update_status(user_id: int, group_id: int, date: str, status: int):
        confirmation = await Confirmation.query.where(and_(Confirmation.member_get == user_id,
                                                           Confirmation.group_id == group_id,
                                                           Confirmation.date == date)).gino.first()
        return await confirmation.update(accept=status).apply()

    @staticmethod
    async def get_member_recieve(group_id, date):
        member = await Confirmation.query.where(and_(Confirmation.group_id == group_id, Confirmation.date == date)).gino.first()
        user = await DBCommands.get_user(member.member_recieve)
        return user

    @staticmethod
    async def change_queue(user_id_from, user_id_to, group_id):
        memeber_to = await Member.query.where(and_(Member.group_id == group_id, Member.member == user_id_to)).gino.first()
        memeber_from = await Member.query.where(and_(Member.group_id == group_id, Member.member == user_id_from)).gino.first()

        if memeber_to and memeber_from:
            queue_to, queue_from = memeber_from.id_queue, memeber_to.id_queue
            await memeber_to.update(id_queue=queue_to).apply()
            await memeber_from.update(id_queue=queue_from).apply()
            return True

        return False

    @staticmethod
    async def get_user(user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def add_language(user_id, lang):
        user = User(user_id=user_id, language=lang)
        await user.create()

    @staticmethod
    async def get_user_with_name(name) -> User:
        user = await User.query.where(User.name == name).gino.first()
        return user

    @staticmethod
    async def get_user_from_member(user_id: int, group_id: int) -> Member:
        group = await Member.query.where(and_(Member.member == user_id, Member.group_id == group_id)).gino.first()
        return group

    @staticmethod
    async def get_group_from_id(group_id) -> Group:
        group = await Group.query.where(Group.id == group_id).gino.first()
        return group

    @staticmethod
    async def get_group_now(user_id, group_id) -> bool:
        group = await Group.query.where(and_(Group.user_id == user_id, Group.id == group_id)).gino.first()
        if group:
            return True
        else:
            return False

    @staticmethod
    async def get_user_from_table_member(user_id: int, group_id: int) -> Member:
        member = await Member.query.where(and_(Member.member == user_id, Member.group_id == group_id)).gino.first()
        return member

    @staticmethod
    async def create_user(user_id,
                          name=None,
                          phone=None,
                          nickname=None,
                          accept=None) -> User:
        new_date = (datetime.today() + timedelta(days=30)).strftime('%d-%m-%Y')
        user = await DBCommands.get_user(user_id=user_id)
        await user.update(name=name, nickname=nickname, phone=phone, accept=accept, end_date=new_date).apply()
        return user

    @staticmethod
    async def language_update(user_id, language):
        user = await User.query.where(User.user_id == user_id).gino.first()
        await user.update(language=language).apply()

    @staticmethod
    async def create_group(user_id, members, name, money, token):
                           # location=str,
                           # start_date=str,
                           # period=str,
                           # link=str,
                           # private=int,
        group = Group(user_id=user_id, name=name, number_of_members=members, amount=money, token=token)
        await group.create()

    @staticmethod
    async def add_member(member: int, group_id: int, id_queue: int) -> bool:
        validate = await Group.query.where(Group.id == group_id).gino.first()
        members = await select([func.count(Member.id)]).where(Member.group_id == group_id).gino.scalar()
        if members is None or validate.number_of_members > members:
            member_obj = Member(member=member, group_id=group_id, id_queue=id_queue)
            await member_obj.create()
            if validate.user_id != member:
                confirm = Confirmation(group_id=group_id, member_recieve=validate.user_id, member_get=member,
                                       date=validate.start_date, accept=0)
                await confirm.create()
            return True
        else:
            return False

    @staticmethod
    async def search_group(token: str) -> Group:
        group = await Group.query.where(Group.token == token).gino.first()
        return group

    @staticmethod
    async def search_group_by_name(name: str) -> Group:
        group = await Group.query.where(Group.name == name).gino.first()
        return group

    @staticmethod
    async def get_all_open_groups(user_id) -> List[Group]:
        groups = await Group.query.where(and_(Group.private != 1, Group.start != 1)).gino.all()
        allowed_groups = []
        for group in groups:
            wrong_members = await Member.query.where(and_(Member.member == user_id, Member.group_id == group.id)).gino.first()
            if wrong_members is not None:
                continue
            members = await db.select([func.count(Member.id)]).where(Member.group_id == group.id).gino.scalar()
            if members is not None and group.number_of_members > members:
                allowed_groups.append(group.name)
        return allowed_groups

    @staticmethod
    async def get_users_name_from_group_id(group_id: int, user_id: int) -> List[str]:
        query = await select([User.name]).select_from(join(Member, User, User.user_id == Member.member)).where(and_(Member.group_id == group_id, Member.member != user_id)).gino.all()
        result = [row[0] for row in query]
        return result

    @staticmethod
    async def get_users_id_from_group_id(group_id: int, user_id: int) -> List[str]:
        query = await select([User.user_id]).select_from(join(Member, User, User.user_id == Member.member)).where(and_(Member.group_id == group_id, Member.member != user_id)).gino.all()
        result = [row[0] for row in query]
        return result

    @staticmethod
    async def do_complain(name: str, group_id: int):
        user = await User.query.select_from(join(Member, User, User.user_id == Member.member)).where(and_(Member.group_id == group_id, User.name == name)).gino.first()
        if user:
            await user.update(complain=user.complain + 1).apply()
            return user

    @staticmethod
    async def settings_update(group_id, key, value):
        value = int(value) if value.isdigit() else value
        group = await Group.update.values(**{key: value}).where(Group.id == group_id).gino.status()
        return group

    @staticmethod
    async def select_user_in_group_id(user_id: int):
        group = await UserInGroup.query.where(UserInGroup.user_id == user_id).gino.first()
        if group:
            return group.group_id

    @staticmethod
    async def update_user_in_group_id(user_id: int, group_id: int):
        user_in_group = await UserInGroup.query.where(UserInGroup.user_id == user_id).gino.first()
        if user_in_group:
            await user_in_group.update(group_id=group_id).apply()
        else:
            user_in_group = UserInGroup(user_id=user_id, group_id=group_id)
            await user_in_group.create()
        return user_in_group

    @staticmethod
    async def select_all_groups(user_id: int, group_id: int) -> List[str]:
        group_names = []
        members = await Member.query.where(and_(Member.member == user_id, Member.group_id != group_id)).gino.all()
        for member in members:
            group = await Group.query.where(Group.id == member.group_id).gino.first()
            group_names.append(group.name)
        return group_names

    @staticmethod
    async def queue(group_id):
        query = await Member.query.where(Member.group_id == group_id).order_by(Member.id_queue.asc()).gino.all()
        return [row.member for row in query]

    @staticmethod
    async def start_button(group_id):
        group = await Group.query.where(Group.id == group_id).gino.first()
        await group.update(start=1).apply()
        return group

    @staticmethod
    async def get_confirmation(group_id, start_date):
        names = []
        accepts = []
        confirmation = await Confirmation.query.where(and_(Confirmation.group_id == group_id, Confirmation.date == start_date)).gino.all()
        confirm = await Confirmation.query.where(and_(Confirmation.group_id == group_id, Confirmation.date == start_date)).gino.first()
        receiver = await User.query.where(User.user_id == confirm.member_recieve).gino.first()
        for user in confirmation:
            us = await User.query.where(User.user_id == user.member_get).gino.first()
            names.append(us.name)
            if user.accept != 1:
                accepts.append("❌")
            else:
                accepts.append("✅")
        return {"receiver": receiver.name, "names": names, "accepts": accepts}














