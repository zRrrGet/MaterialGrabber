from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

from src.tgbot.config import Config
from src.tgbot.misc.states import MainDialogSG


async def user_start(message: Message, dialog_manager: DialogManager, config: Config):
    await message.answer(config.misc.start_text)
    await dialog_manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
