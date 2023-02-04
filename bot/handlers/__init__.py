from aiogram import Dispatcher

from .handlers import start


def setup(dp: Dispatcher):
    """
    Setup handlers
    """

    dp.register_message_handler(start, commands=["start"])