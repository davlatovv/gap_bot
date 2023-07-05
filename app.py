import aioschedule as aioschedule
from utils.db_api.db_commands import DBCommands
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db
import asyncio


async def scheduler():
    await DBCommands.process_groups()
    aioschedule.every().day.at('00:01').do(DBCommands.process_groups)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(86400)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    await create_db()

    asyncio.create_task(scheduler())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)










