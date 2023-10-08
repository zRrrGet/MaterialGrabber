from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from aiogram_dialog import DialogManager, StartMode
from src.tgbot.misc.states import MainDialogSG


async def on_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)


async def on_chat(message: Message, dialog_manager: DialogManager):
    await message.answer('<a href="https://google.com">Здесь</a> вы можете пообщаться с пользователями бота '
                         'и задать все интересующие вопросы.')


async def on_donate(message: Message, dialog_manager: DialogManager):
    await message.answer('В разработке...')


def register_user(dp: Dispatcher):
    router = Router()
    dp.include_router(router)

    router.message.register(on_start)
    dp.message.register(on_start, CommandStart())
    dp.message.register(on_chat, Command('chat'))
    dp.message.register(on_donate, Command('donate'))
