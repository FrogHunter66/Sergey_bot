import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.models import db
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TELEGRAM_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)
__all__ = ['bot', 'storage', 'dp', 'db']
