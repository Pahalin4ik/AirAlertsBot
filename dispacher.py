import os
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=storage)
