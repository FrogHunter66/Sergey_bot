import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import group_game
from handlers.admins import create_event, utils, create_test, first, commands_for_tests, second
from config import TELEGRAM_TOKEN
import logging

from utils.db_api.database import connect, disconnect
from utils.models import create_tables
from utils.db_api.quck_commands.event import add_event

async def main():
    await create_tables()
    try:
        logging.basicConfig(level=logging.INFO)
        storage = MemoryStorage()
        bot = Bot(token=TELEGRAM_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_routers(create_event.router, utils.router, create_test.router, first.router, commands_for_tests.router, second.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await disconnect()


if __name__ == "__main__":
    asyncio.run(main())
