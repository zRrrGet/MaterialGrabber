from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Cancel
from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.tgbot.misc.states import SubAlertDialogSG
from src.core.external.controllers.user_controller import UserController


async def on_validate(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']

    if await user_controller.is_subscribed(manager):
        await manager.switch_to(SubAlertDialogSG.exit_text, show_mode=ShowMode.SEND)
    else:
        await callback.message.answer('Чтобы продолжить, нужно подписаться на спонсорский канал')


async def channels_getter(user_controller: UserController, dialog_manager: DialogManager, **kwargs):
    return {
        'channels': await user_controller.get_unsubscribed_channels(dialog_manager)
    }


sub_alert_dialog = Dialog(
    Window(

        Const('Вам не нужно тратить время на выбор области водяного знака для удаления. '
              'YOLICO бот определяет это автоматически.\n\n'

              'Бот YOLICO сохраняет исходное качество вашего изображения без потери деталей.\n\n'

              'Для удаления водяных знаков не требуется никаких навыков редактирования видео/фото.\n'
              'Вы можете сделать это без особых усилий, используя нашего уникального бота.\n\n'

              '<a href="https://google.com">FAQ</a>\n\n'

              'Для того, чтобы бесплатно пользоваться ботом YOLICO, нужно подписаться на канал спонсора.\n\n'

              'Скорее нажимайте «Подписаться», подписывайтесь, и начинайте!'),

        SwitchTo(Const('Подписаться'), id='to_sub_control', state=SubAlertDialogSG.sub_control),
        state=SubAlertDialogSG.warn_text,
    ),
    Window(
        Const('Спонсорский канал:'),
        List(
            Format('- {item[0]}'),
            items='channels',
        ),
        Button(Const('Проверить подписку'), id='check_sub', on_click=on_validate),
        getter=channels_getter,
        state=SubAlertDialogSG.sub_control,
    ),
    Window(
        Const('Спасибо за подписку, теперь вы можете '
              'воспользоваться нашими бесплатными услугами 👇👇👇'),
        Cancel(Const('Меню')),
        state=SubAlertDialogSG.exit_text,
    )
)
