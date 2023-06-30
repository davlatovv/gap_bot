import asyncio
import schedule
from aiogram import Bot, Dispatcher, types
from handlers import dp
from utils.db_api.db_commands import DBCommands
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db
#
#
# async def on_startup(dp: Dispatcher):
#     import filters
#     import middlewares
#     filters.setup(dp)
#     middlewares.setup(dp)
#
#     await set_default_commands(dp)
#     await on_startup_notify(dp)
#
#     await create_db()
#
#
# def job():
#     asyncio.run(DBCommands.process_gaps())
#
#
# async def start_scheduler():
#     while True:
#         schedule.run_pending()
#         await asyncio.sleep(1)
#
#
# async def main():
#     scheduler_task = asyncio.create_task(start_scheduler())
#     bot_task = asyncio.create_task(dp.start_polling(skip_updates=True, on_startup=on_startup))
#     await scheduler_task
#     await bot_task
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
# async def on_startup(dp):
#     import filters
#     import middlewares
#     filters.setup(dp)
#     middlewares.setup(dp)
#
#     await set_default_commands(dp)
#     await on_startup_notify(dp)
#
#     await create_db()
#
#
# if __name__ == '__main__':
#     from aiogram import executor
#     from handlers import dp
#
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

import schedule
import time
import asyncio


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    await create_db()


async def process():
    await DBCommands.process_gaps()


def run_process_gaps():
    asyncio.run(process())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    schedule.every().day.at("02:24").do(run_process_gaps)


    async def schedule_jobs():
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)


    asyncio.create_task(schedule_jobs())
    loop = asyncio.get_event_loop()
    loop.run_forever()
