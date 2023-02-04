from aiogram.dispatcher.handler import Handler
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def start(message: Message):
    """
    Example handler function
    """
    await message.answer('Select account for which you want to get Steam Guard pass')
