import os
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from bot import handlers

from aiohttp import web

from dotenv import load_dotenv

from models.models import *


async def start_web_server():
    app = web.Application()
    # setup your web routes here
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()


async def on_startup(dp):
    # Setup handlers
    handlers.setup(dp)


async def on_shutdown(dp, bot):
    print('Stoping...')


def main():
    db.connect()
    Accounts.create_table()
    WhiteList.create_table()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    bot = loop.run_until_complete(on_startup(dp))
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    load_dotenv()
    main()
