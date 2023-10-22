from typing import Any

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Group, Url, Start, Back, SwitchTo

from src.tgbot.misc.states import MainDialogSG, DownloaderDialogSG, SubAlertDialogSG, RulesAgreementDialogSG
from src.core.external.controllers.user_controller import UserController
from src.core.external.controllers.day_limit_controller import DayLimitController


async def limit_getter(day_limit_controller: DayLimitController, user_id: int, dialog_manager: DialogManager,
                       **kwargs):
    day_req_limit = day_limit_controller.get_limit(user_id)

    limit_text = f'<b>Доступные генерации:</b> {day_req_limit.left_requests}'
    if not day_req_limit.left_requests:
        limit_text += (f'\nСледующая генерация будет доступна: '
                       f'{day_req_limit.next_request_time.strftime("%d-%m-%Y %H:%M:%S")}')

    return {
        'show_limit': day_req_limit.day_limit != -1,
        'day_limit_text': limit_text
    }


async def run_pre_dialogs(manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']

    if not await user_controller.is_subscribed(manager):
        await manager.start(SubAlertDialogSG.warn_text, show_mode=ShowMode.SEND)

    elif not user_controller.are_rules_accepted(manager):
        await manager.start(RulesAgreementDialogSG.main, show_mode=ShowMode.SEND)


async def on_process_result(start_data: dict, result: Any, dialog_manager: DialogManager):
    await run_pre_dialogs(dialog_manager)


async def on_dialog_start(start_data: dict, manager: DialogManager):
    await run_pre_dialogs(manager)


main_dialog = Dialog(
    Window(
        Const('<b>Главное меню</b>\n\nДля использования бота нейросети YOLICO перейдите во вкладку '
              '«<b>Удалить водяные знаки</b>».\n'),

        Format('{day_limit_text}', when='show_limit'),

        Start(Const('🔷 Удалить водяные знаки 🔷'), id='downloader_dialog', state=DownloaderDialogSG.main),
        Group(
            SwitchTo(Const('Реферальная программа'), id='ref_dialog', state=MainDialogSG.in_dev),
            SwitchTo(Const('Чат'), id='chat_url', state=MainDialogSG.in_dev),
            SwitchTo(Const('Тех. помощь'), id='support_dialog', state=MainDialogSG.in_dev),
            SwitchTo(Const('Вопрос-ответ'), id='faq_url', state=MainDialogSG.in_dev),
            width=2),
        getter=limit_getter,
        state=MainDialogSG.main
    ),
    Window(
        Const('В разработке...'),
        Back(Const('◀ Назад')),
        state=MainDialogSG.in_dev
    ),
    on_start=on_dialog_start,
    on_process_result=on_process_result
)
