from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from src.tgbot.filters.admin import AdminFilter


async def admin_start(message: Message):
    await message.reply('Hello, admin!')


def register_admin(dp: Dispatcher):
    dp.message.register(admin_start, Command('admin'), AdminFilter(True))
