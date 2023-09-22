from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from src.tgbot.misc.states import MainDialogSG, SubAlertDialogSG
from src.core.external.controllers.user_controller import UserController


async def on_validate(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']
    if await user_controller.is_subscribed(callback):
        await manager.start(MainDialogSG.main, mode=StartMode.RESET_STACK)
    else:
        await callback.message.answer('Нет подписки - нет доступа :(')


async def channels_getter(user_controller: UserController, dialog_manager: DialogManager, **kwargs):
    return {
        'channels': await user_controller.get_unsubscribed_channels(dialog_manager)
    }


sub_alert_dialog = Dialog(
    Window(
        Const('Хренушки тебе, нужно подписаться на какие-то каналы:'),
        List(
            Format('- {item[0]}'),
            items='channels',
        ),
        Button(Const('Проверить подписку'), id='check_sub', on_click=on_validate),
        getter=channels_getter,
        state=SubAlertDialogSG.main,
    )
)
