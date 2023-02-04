import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import Handler
from aiogram.types import ParseMode
from aiogram.utils import executor

from bot import handlers


async def on_startup(dp):
    handlers.setup(dp)
    logging.log(1, msg='handlers setuped')


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")


if __name__ == '__main__':
    load_dotenv()
    API_TOKEN = os.getenv('BOT_TOKEN')

    # Configure logging
    bot = Bot(API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
