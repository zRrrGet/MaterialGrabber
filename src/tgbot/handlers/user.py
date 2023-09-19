from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

from src.core.external.controllers.user_controller import UserController

from src.tgbot.config import Config
from src.tgbot.misc.states import MainDialogSG


async def user_start(message: Message, dialog_manager: DialogManager, config: Config, user_controller: UserController):
    user_controller.ensure_user(message)
    await message.answer(config.misc.start_text)

    if user_controller.is_user_subscribed(message):
        await dialog_manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)
    else:
        await message.answer('хрен тебе')


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
