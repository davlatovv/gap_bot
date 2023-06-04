from .models import User


class DBCommands:
    @staticmethod
    async def get_user(user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def create_user(user_id, name=None, phone=None, language=None, nickname=None, sms=None, accept=None) -> User:
        user = User(user_id=user_id, name=name, nickname=nickname, phone=phone, language=language, sms=sms, accept=accept)
        await user.create()
        return user

    # @staticmethod
    # async def create_group(cash, name):
    #     user =



