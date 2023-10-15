from aiogram import Dispatcher, Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram_dialog import DialogManager, StartMode
from src.tgbot.misc.states import MainDialogSG, DownloaderDialogSG


async def on_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)


async def on_start_button(query: CallbackQuery, bot: Bot, dialog_manager: DialogManager):
    await dialog_manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    router = Router()
    dp.include_router(router)
    router.message.register(on_start)

    dp.callback_query.register(on_start_button, F.data == 'on_start')
    dp.message.register(on_start, CommandStart())
