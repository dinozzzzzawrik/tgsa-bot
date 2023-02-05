from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message
from models.models import WhiteList


async def help(msg: Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)
        await msg.answer('Admin-panel: url')
    except (Exception,):
        await msg.answer('Bot to get Steam Guard Code with telegram\n'
                         'GitHub with projects parts: https://github.com/dinozzzzzawrik')
