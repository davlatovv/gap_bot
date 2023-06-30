from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_, select

from .models import User, Gap, Member, UserInGap, Confirmation


class DBCommands:
    @staticmethod
    async def process_gaps():
        today = datetime.today().strftime('%d/%m/%Y')
        gaps = await Gap.query.gino.all()

        for gap in gaps:
            queue_members = await DBCommands.queue(gap_id=gap.id)
            await gap.update(start_date=today).apply()

            if gap.start_date == today:
                new_date = (datetime.today() + timedelta(days=gap.period)).strftime('%d/%m/%Y')
                await gap.update(start_date=new_date).apply()

                for i, member in enumerate(queue_members):
                    if i == 0:
                        update_id = await Member.query.where(
                            and_(Member.gap_id == gap.id, Member.member == member)).gino.first()
                        last_id = await Member.query.where(
                            and_(Member.gap_id == gap.id, Member.member == queue_members[-1])).gino.first()
                        await update_id.update(id_queue=last_id.id_queue).apply()
                    else:
                        confirm = Confirmation(gap_id=gap.id, member_recieve=queue_members[0], member_get=member,
                                               date=new_date)
                        await confirm.create()

                        update_id = await Member.query.where(
                            and_(Member.gap_id == gap.id, Member.member == member)).gino.first()
                        await update_id.update(id_queue=update_id.id_queue - 1).apply()

    # @staticmethod
    # async def process_gaps():
    #     today = datetime.today().strftime('%d-%m-%Y')
    #     gaps = await Gap.query.gino.all()
    #     for gap in gaps:
    #         queue_members = await DBCommands.queue(gap_id=gap.id)
    #         if gap.start_date == today:
    #             new_date = gap.start_date + timedelta(days=gap.period)
    #             gap.update(start_date=new_date)
    #             for member in queue_members:
    #                 if member is queue_members[0]:
    #                     update_id = await Member.query.where(and_(Member.gap_id == gap.id, Member.member == member)).gino.first()
    #                     last_id = await Member.query.where(and_(Member.gap_id == gap.id, Member.member == queue_members[-1])).gino.first()
    #                     await update_id.update(id=last_id.id)
    #                 else:
    #                     confirm = Confirmation(gap_id=gap.id, member_recieve=queue_members[0], member_get=member, date=new_date)
    #                     await confirm.create()
    #                     update_id = await Member.query.where(and_(Member.gap_id == gap.id, Member.member == member)).gino.first()
    #                     await update_id.update(id=update_id.id+1)







    @staticmethod
    async def get_user(user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def get_user_with_name(name) -> User:
        user = await User.query.where(User.name == name).gino.first()
        return user

    @staticmethod
    async def get_gap(user_id) -> Gap:
        gap = await Gap.query.where(Gap.user_id == user_id).gino.first()
        return gap

    @staticmethod
    async def get_gap_from_id(gap_id) -> Gap:
        gap = await Gap.query.where(Gap.id == gap_id).gino.first()
        return gap

    @staticmethod
    async def get_gap_now(user_id, gap_id) -> bool:
        gap = await Gap.query.where(and_(Gap.user_id == user_id, Gap.id == gap_id)).gino.first()
        if gap:
            return True
        else:
            return False

    @staticmethod
    async def get_join(user_id, gap_id) -> bool:
        member = await Member.query.where(and_(Member.member == user_id, Member.gap_id != gap_id)).gino.first()
        if member:
            return True

    @staticmethod
    async def create_user(user_id,
                          name=None,
                          phone=None,
                          language=None,
                          nickname=None,
                          sms=None,
                          accept=None) -> User:
        user = User(user_id=user_id, name=name, nickname=nickname, phone=phone,
                    language=language, sms=sms, accept=accept)
        await user.create()
        return user

    @staticmethod
    async def create_group(user_id=int,
                           name=str,
                           members=int,
                           money=str,
                           location=str,
                           start_date=str,
                           period=str,
                           link=str,
                           private=int,
                           token=str) -> Gap:
        gap = Gap(user_id=user_id, name=name, number_of_members=members, amount=money,
                  location=location, link=link, private=private, start_date=start_date, period=period, token=token)
        await gap.create()
        return gap

    @staticmethod
    async def add_member(member: int, gap_id: int) -> bool:
        validate = await Gap.query.where(Gap.id == gap_id).gino.first()
        members = await Member.query.where(Member.gap_id == gap_id).gino.scalar()
        if members is None or validate.number_of_members > members:
            member_obj = Member(member=member, gap_id=gap_id)
            await member_obj.create()
            return True
        else:
            return False

    @staticmethod
    async def search_group(token: str) -> Gap:
        gap = await Gap.query.where(Gap.token == token).gino.first()
        return gap

    @staticmethod
    async def search_group_by_name(name: str) -> Gap:
        gap = await Gap.query.where(Gap.name == name).gino.first()
        return gap

    @staticmethod
    async def get_all_members(gap_id: int, user_id: int) -> List[str]:
        members = await Member.query.where(Member.gap_id == gap_id).gino.all()
        member_ids = [member.member for member in members if member.member != user_id]
        member_names = [await User.query.where(User.user_id == user_id).gino.first() for user_id in member_ids]
        return [name.name for name in member_names]

    @staticmethod
    async def get_all_members_queue(gap_id: int) -> List[str]:
        members = await Member.query.where(Member.gap_id == gap_id).gino.all()
        member_ids = [member.member for member in members]
        member_names = [await User.query.where(User.user_id == user_id).gino.first() for user_id in member_ids]
        return [name.name for name in member_names]

    @staticmethod
    async def do_complain(name: str):
        user = await User.query.where(User.name == name).gino.first()
        if user:
            await user.update(complain=user.complain + 1).apply()
        else:
            return "Такого пользователя нет в базе данных"

    @staticmethod
    async def select_user_in_gap_id(user_id: int):
        gap = await UserInGap.query.where(UserInGap.user_id == user_id).gino.first()
        if gap:
            return gap.gap_id

    @staticmethod
    async def update_user_in_gap_id(user_id: int, gap_id: int):
        user_in_gap = await UserInGap.query.where(UserInGap.user_id == user_id).gino.first()
        if user_in_gap:
            await user_in_gap.update(gap_id=gap_id).apply()
        else:
            user_in_gap = UserInGap(user_id=user_id, gap_id=gap_id)
            await user_in_gap.create()
        return user_in_gap

    @staticmethod
    async def select_all_gaps(user_id: int, gap_id: int) -> List[str]:
        gap_names = []
        members = await Member.query.where(and_(Member.member == user_id, Member.gap_id != gap_id)).gino.all()
        for member in members:
            gap = await Gap.query.where(Gap.id == member.gap_id).gino.first()
            gap_names.append(gap.name)
        return gap_names

    @staticmethod
    async def queue(gap_id):
        query = await Member.query.where(Member.gap_id == gap_id).order_by(Member.id_queue.asc()).gino.all()
        return [row.member for row in query]

    @staticmethod
    async def start_button(gap_id):
        gap = await Gap.query.where(Gap.id == gap_id).gino.first()
        await gap.update(start=gap.start+1).apply()
        return gap















