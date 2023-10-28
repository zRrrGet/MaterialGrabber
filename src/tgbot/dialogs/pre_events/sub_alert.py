import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Url, ListGroup
from aiogram_dialog import DialogManager, ShowMode

from src.tgbot.misc.states import SubAlertDialogSG
from src.core.external.controllers.user_controller import UserController


async def on_validate(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']

    if await user_controller.is_subscribed(manager):
        await callback.message.delete()
        await manager.done(manager.dialog_data['garbage_msg_ids'], show_mode=ShowMode.SEND)
    else:
        msg = await callback.message.answer('Чтобы продолжить, нужно подписаться на канал.')
        manager.dialog_data['garbage_msg_ids'].append(msg.message_id)


async def channels_getter(user_controller: UserController, dialog_manager: DialogManager, **kwargs):
    return {
        'channels': await user_controller.get_unsubscribed_channels(dialog_manager)
    }


async def on_dialog_start(start_data: dict, manager: DialogManager):
    manager.dialog_data['garbage_msg_ids'] = []


sub_alert_dialog = Dialog(
    Window(

        Const('Теперь не нужно тратить время на выбор области водяного знака для удаления. '
              'YOLICO бот определяет это автоматически.\n\n'

              'Бот YOLICO сохраняет исходное качество вашего фото/видео без потери деталей.\n\n'

              'Для того, чтобы бесплатно пользоваться ботом YOLICO, нужно подписаться на канал.\n\n'

              'Скорее подписывайтесь, нажимайте «Подписался ✅» и начинайте!'),

        ListGroup(
            Url(Const('Канал'), Format('{item[0]}')),
            id='channels_list',
            item_id_getter=operator.itemgetter(0),
            items='channels'
        ),

        Button(Const('Подписался ✅'), id='check_sub', on_click=on_validate),
        getter=channels_getter,
        state=SubAlertDialogSG.warn_text,
    ),
    on_start=on_dialog_start,
)
