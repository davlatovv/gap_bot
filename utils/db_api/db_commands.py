from .models import User, Gap, Member


class DBCommands:
    @staticmethod
    async def get_user(user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def get_gap(user_id) -> Gap:
        gap = await Gap.query.where(Gap.user_id == user_id).gino.first()
        return gap

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
    async def add_member(member=int) -> Member:
        gap = await DBCommands.get_gap(member)
        role = Member(member=member, gap_id=gap.id)
        await role.create()
        return role

    @staticmethod
    async def search_group(token=str) -> Gap:
        gap = await Gap.query.where(Gap.token == token).gino.first()
        return gap




