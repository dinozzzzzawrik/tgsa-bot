import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from steampy.guard import generate_one_time_code

from dotenv import load_dotenv

from models import *


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    whitelist = WhiteList.select(WhiteList.tg_id)
    if msg.from_user.id in whitelist:

        greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        accounts = Accounts.select()

        for acc in accounts:
            button = KeyboardButton(acc.name)
            greet_kb2.add(button)

        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram', reply_markup=greet_kb2)
    else:
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    whitelist = WhiteList.select(WhiteList.tg_id)
    if msg.from_user.id in whitelist:
        await msg.reply('Admin-panel: url')
    else:
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


@dp.message_handler()
async def get_code(msg: types.Message):
    whitelist = WhiteList.select(WhiteList.tg_id)
    if msg.from_user.id in whitelist:
        try:
            account = Accounts.select().where(Accounts.name == msg.text).get()
            one_time_authentication_code = generate_one_time_code(account.key)
            await bot.send_message(msg.from_user.id, f'Steam Guard: {one_time_authentication_code}')
        except (Exception,):
            await bot.send_message(msg.from_user.id, 'this account is not in data base')
    else:
        await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram\n'
                                                 'GitHub with projects parts: https://github.com/dinozzzzzawrik')


if __name__ == '__main__':
    db.connect()
    Accounts.create_table()
    WhiteList.create_table()
    executor.start_polling(dp)
