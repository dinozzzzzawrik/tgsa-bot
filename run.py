import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Bot to get Steam Guard Code with telegram')


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    await msg.reply('Admin-panel: url')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
