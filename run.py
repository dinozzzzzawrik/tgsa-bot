import os
import asyncio
import jinja2
import base64
import fernet
import aiohttp_session
import aiohttp_jinja2


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

from aiohttp_session.cookie_storage import EncryptedCookieStorage


def setup_routes(application: web.Application) -> None:
    from web.admin.routes import setup_routes as setup_web_routes
    setup_web_routes(application)


async def setup_app(application: web.Application) -> None:
    setup_routes(application)


async def start_web_server():
    app = web.Application()
    runner = web.AppRunner(app)
    await setup_app(app)
    # session_key = base64.urlsafe_b64decode(fernet.Fernet.generate_key())
    # setup(app, cookie_storage=EncryptedCookieStorage(session_key))
    app.middlewares.append(aiohttp_session.session_middleware(aiohttp_session.SimpleCookieStorage()))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('web/templates'))
    await runner.setup()
    site = web.TCPSite(runner, host=None, port=os.getenv('PORT'))
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
