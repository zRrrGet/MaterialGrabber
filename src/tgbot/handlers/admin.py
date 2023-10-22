from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from src.tgbot.filters.admin import AdminFilter
from src.core.external.controllers.user_controller import UserController


async def on_reset_sub(message: Message, user_controller: UserController):
    user_controller.reset_sub_all()
    await message.reply('Проверка подписок была успешно обнулена.')


def register_admin(dp: Dispatcher):
    dp.message.register(on_reset_sub, Command('reset_sub'), AdminFilter(True))
