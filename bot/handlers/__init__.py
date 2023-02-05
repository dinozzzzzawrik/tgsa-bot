from aiogram import Dispatcher

from .private.start import start
from .private.help import help
from .private.code import get_sg_code


def setup(dp: Dispatcher):
    """
    Setup handlers
    """

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(get_sg_code)
