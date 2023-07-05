from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_, select, join, desc, func

from text import no, yes
from .models import User, Gap, Member, UserInGap, Confirmation


class DBCommands:
    @staticmethod
    async def process_gaps():
        today = datetime.today().strftime('%d/%m/%Y')
        gaps = await Gap.query.gino.all()

        for gap in gaps:
            queue_members = await DBCommands.queue(gap_id=gap.id)

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
                                               date=new_date, accept=0)
                        await confirm.create()

                        update_id = await Member.query.where(
                            and_(Member.gap_id == gap.id, Member.member == member)).gino.first()
                        await update_id.update(id_queue=update_id.id_queue - 1).apply()

    @staticmethod
    async def get_queue(gap_id: int):
        queue = await Member.query.where(Member.gap_id == gap_id).order_by(desc(Member.id_queue)).gino.first()
        return queue

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
        member = await Member.query.where(and_(Member.member == user_id, Member.gap_id == gap_id)).gino.first()
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
    async def add_member(member: int, gap_id: int, id_queue: int) -> bool:
        validate = await Gap.query.where(Gap.id == gap_id).gino.first()
        members = await select([func.count(Member.id)]).where(Member.gap_id == gap_id).gino.scalar()
        if members is None or validate.number_of_members > members:
            member_obj = Member(member=member, gap_id=gap_id, id_queue=id_queue)
            await member_obj.create()
            if validate.user_id != member:
                confirm = Confirmation(gap_id=gap_id, member_recieve=validate.user_id, member_get=member,
                                       date=validate.start_date, accept=0)
                await confirm.create()
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
    async def get_users_name_from_gap_id(gap_id: int, user_id: int) -> List[str]:
        query = await select([User.name]).select_from(join(Member, User, User.user_id == Member.member)).where(and_(Member.gap_id == gap_id, Member.member != user_id)).gino.all()
        result = [row[0] for row in query]
        return result

    @staticmethod
    async def get_all_members_queue(gap_id: int) -> List[str]:
        members = await Member.query.where(Member.gap_id == gap_id).gino.all()
        member_ids = [member.member for member in members]
        member_names = [await User.query.where(User.user_id == user_id).gino.first() for user_id in member_ids]
        return [name.name for name in member_names]

    @staticmethod
    async def do_complain(name: str, gap_id: int):
        user = await User.query.select_from(join(Member, User, User.user_id == Member.member)).where(and_(Member.gap_id == gap_id, User.name == name)).gino.first()
        if user:
            await user.update(complain=user.complain + 1).apply()

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
        await gap.update(start=1).apply()
        return gap

    @staticmethod
    async def get_confirmation(gap_id, start_date):
        names = []
        accepts = []
        confirmation = await Confirmation.query.where(and_(Confirmation.gap_id == gap_id, Confirmation.date == start_date)).gino.all()
        confirm = await Confirmation.query.where(and_(Confirmation.gap_id == gap_id, Confirmation.date == start_date)).gino.first()
        receiver = await User.query.where(User.user_id == confirm.member_recieve).gino.first()
        for user in confirmation:
            us = await User.query.where(User.user_id == user.member_get).gino.first()
            names.append(us.name)
            if user.accept is not 1:
                accepts.append(no)
            else:
                accepts.append(yes)
        return {"receiver": receiver.name, "names": names, "accepts": accepts}














