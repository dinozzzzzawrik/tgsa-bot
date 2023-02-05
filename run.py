import os
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from steampy.guard import generate_one_time_code, generate_confirmation_key

from aiohttp import web

from dotenv import load_dotenv

from models import *


load_dotenv()

dp = Dispatcher(Bot(token=os.getenv('BOT_TOKEN')))


async def start_web_server():
    app = web.Application()
    # setup your web routes here
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()


async def on_startup(dp):
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    # setup your handlers here
    return bot


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.close()


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        accounts = Accounts.select()

        for acc in accounts:
            button = KeyboardButton(acc.name)
            kb.add(button)

        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram', reply_markup=kb)
    except (Exception,):
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)
        await msg.reply('Admin-panel: url')
    except (Exception,):
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


@dp.message_handler()
async def get_sg_code(msg: types.Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)
        try:
            account = Accounts.select().where(Accounts.name == msg.text).get()
            one_time_authentication_code = generate_one_time_code(account.key)
            await bot.send_message(msg.from_user.id, f'Steam Guard: {one_time_authentication_code}')
        except (Exception,):
            await bot.send_message(msg.from_user.id, 'this account is not in data base')
    except (Exception,):
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


if __name__ == '__main__':
    db.connect()
    Accounts.create_table()
    WhiteList.create_table()
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    bot = loop.run_until_complete(on_startup(dp))
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
