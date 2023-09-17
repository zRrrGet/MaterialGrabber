from aiogram import Dispatcher

from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog.api.exceptions import UnknownIntent


async def unknown_control(event: ErrorEvent):
    err_text = 'Похоже, вы взаимодействуете с уже недействительным элементом управления :('
    await event.update.callback_query.message.answer(err_text)


def register_all_error_handlers(dp: Dispatcher):
    dp.error.register(unknown_control, ExceptionTypeFilter(UnknownIntent))
