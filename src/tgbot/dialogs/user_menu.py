import operator
from typing import Any

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Group, Button, Select
from aiogram_dialog.widgets.input import MessageInput

from src.tgbot.misc.states import MainDialogSG, SubAlertDialogSG, ProgressObserverDialogSG
from src.core.external.controllers.downloader_controller import DownloaderController

from src.core.domain.exceptions.handler_req_ex import *


async def on_input_link(m: Message, widget: MessageInput, manager: DialogManager):
    downloader_controller: DownloaderController = manager.middleware_data['downloader_controller']
    user_id = manager.middleware_data['user_id']
    await manager.done()

    try:
        req_id = await downloader_controller.request_download(user_id, m)
        await manager.start(ProgressObserverDialogSG.main,
                            data={'req_id': req_id, 'req_msg': m},
                            mode=StartMode.NEW_STACK)
    except SubValidationException:
        await manager.start(SubAlertDialogSG.main, mode=StartMode.RESET_STACK)
    except DayLimitException as ex:
        await m.answer(f'Превышен дневной лимит на скачивание!\nВам доступно: {ex.limit} за день')
    except ParallelLimitException as ex:
        await m.answer(f'Превышен лимит на одновременное скачивание!\nВам доступно: {ex.limit} за раз')


async def on_site_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, item: str):
    await manager.switch_to(MainDialogSG.download_link_input)


async def sites_getter(**kwargs):
    sites = ['depositphotos.com',
             'elements.envato.com',
             'istockphoto.com',
             'eyeem.com',
             'gettyimages.de',
             'motionarray.com',
             'shutterstock.com',
             'storyblocks.com',
             'videezy.com',
             'videohive.net']

    return {
        'sites': list(map(lambda c: [c], sites))
    }


main_dialog = Dialog(
    Window(
        Const('Выберите сервис, с которого необходимо скачать материалы'),
        Group(
            Select(
                Format('{item[0]}'),
                id='site_list',
                item_id_getter=operator.itemgetter(0),
                items='sites',
                on_click=on_site_selected
            ),
            width=2
        ),
        state=MainDialogSG.main,
        getter=sites_getter
    ),
    Window(
        Const('Введите ссылку:'),
        MessageInput(on_input_link),
        state=MainDialogSG.download_link_input
    )
)
