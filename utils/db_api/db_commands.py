from typing import List

from sqlalchemy import and_

from .models import User, Gap, Member, UserInGap


class DBCommands:
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
    async def get_gap_now(user_id, gap_id) -> bool:
        gap = await Gap.query.where(and_(Gap.user_id == user_id, Gap.id == gap_id)).gino.first()
        if gap:
            return True
        else:
            return False

    @staticmethod
    async def get_join(user_id) -> Member:
        member = await Member.query.where(Member.member == user_id).gino.first()
        return member

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
                           start=str,
                           period=str,
                           link=str,
                           private=int,
                           token=str) -> Gap:
        gap = Gap(user_id=user_id, name=name, number_of_members=members, amount=money,
                  location=location, link=link, private=private, start=start, period=period, token=token)
        await gap.create()
        return gap

    @staticmethod
    async def add_member(member: int, gap_id: int) -> Member:
        role = Member(member=member, gap_id=gap_id)
        await role.create()
        return role

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
        print([name.name for name in member_names])
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

        members = await Member.query.where(Member.member == user_id).gino.all()
        gaps = await Gap.query.where(and_(Gap.user_id == user_id, Gap.id != gap_id)).gino.all()

        for member in members:
            gap = await Gap.query.where(and_(Gap.id == member.gap_id, Gap.id != gap_id)).gino.first()
            gap_names.append(gap.name)

        for gap in gaps:
            gap_names.append(gap.name)

        return gap_names














