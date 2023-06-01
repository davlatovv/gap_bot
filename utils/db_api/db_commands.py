from .models import User


class DBCommands:
    @staticmethod
    async def get_user(user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def create_user(user_id, name=None, phone=None, language=None, nickname=None, sms=None) -> User:
        user = User(user_id=user_id, name=name, nickname=nickname, phone=phone, language=language, sms=sms)
        await user.create()
        return user

    @staticmethod
    async def update_name(user_id, name):
        user = await User.query.where(User.user_id == user_id).gino.first()
        if user:
            await user.update(name=name).apply()




