from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message
from models.models import WhiteList, Accounts
from steampy.guard import generate_one_time_code, generate_confirmation_key


async def get_sg_code(msg: Message):
    try:
        WhiteList.get(WhiteList.tg_id == msg.from_user.id)
        try:
            account = Accounts.select().where(Accounts.name == msg.text).get()
            one_time_authentication_code = generate_one_time_code(account.key)
            await msg.answer(f'Steam Guard: {one_time_authentication_code}')
        except (Exception,):
            await msg.answer('this account is not in data base')
    except (Exception,):
        await msg.answer('Bot to get Steam Guard Code with telegram\n'
                         'GitHub with projects parts: https://github.com/dinozzzzzawrik')
