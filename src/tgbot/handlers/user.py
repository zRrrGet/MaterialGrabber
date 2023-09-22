from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

from src.core.external.controllers.user_controller import UserController

from src.tgbot.config import Config
from src.tgbot.misc.states import MainDialogSG, SubAlertDialogSG


async def user_start(message: Message, dialog_manager: DialogManager, config: Config, user_controller: UserController):
    user_controller.ensure_user(message)
    await message.answer(config.misc.start_text)

    start_dialog = MainDialogSG.main if await user_controller.is_subscribed(message) else SubAlertDialogSG.main
    await dialog_manager.start(start_dialog, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
