from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message
from models.models import WhiteList, Accounts


async def start(msg: Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        accounts = Accounts.select()

        for acc in accounts:
            button = KeyboardButton(acc.name)
            kb.add(button)

        await msg.answer('Bot to get Steam Guard Code with telegram', reply_markup=kb)
    except (Exception,):
        await msg.answer('Bot to get Steam Guard Code with telegram\n'
                         'GitHub with projects parts: https://github.com/dinozzzzzawrik')
