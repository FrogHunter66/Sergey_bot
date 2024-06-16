import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.admins import create_event, utils, create_test, first, commands_for_tests, second, reuild_question, buy_admin
from handlers.admins.users import register, passing_test
from config import TELEGRAM_TOKEN
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from utils.db_api.database import connect, disconnect
from utils.models import create_tables
from utils.db_api.quck_commands.event import add_event
bot = Bot(token=TELEGRAM_TOKEN)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start', description='Начало работы'
        ),
        BotCommand(command="buy", description="Приобрести возможность создавать тесты")
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def main():
    await create_tables()
    await set_commands(bot)
    try:
        logging.basicConfig(level=logging.INFO)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        dp.include_routers(create_event.router, utils.router, create_test.router, first.router, commands_for_tests.router, second.router, reuild_question.router, buy_admin.router, register.router, passing_test.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await disconnect()


if __name__ == "__main__":
    asyncio.run(main())
