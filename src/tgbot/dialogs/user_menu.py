import asyncio
import operator
from typing import Any

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Group, Button, Select, Back
from aiogram_dialog.widgets.input import MessageInput

from .progress_observer import build_download_keyboard
from src.tgbot.misc.states import MainDialogSG, SubAlertDialogSG, RulesAgreementDialogSG, ProgressObserverDialogSG

from src.core.external.controllers.user_controller import UserController
from src.core.external.controllers.downloader_controller import DownloaderController

from src.core.domain.entities.download_request import ContentType
from src.core.domain.exceptions.req_handler import *
from src.core.domain.exceptions.downloader import *

from .progress_observer import get_err_msg


def get_supported_sites() -> dict:
    return {
        'depositphotos.com': (True, True),
        'elements.envato.com': (True, False),
        'istockphoto.com': (True, True),
        'eyeem.com': (True, False),
        'gettyimages.com': (True, True),
        'motionarray.com': (True, False),
        'shutterstock.com': (True, False),
        'storyblocks.com': (True, True),
        'videezy.com': (False, True)
    }


def get_content_types() -> dict:
    return {'Фото': ContentType.photo,
            'Видео': ContentType.video}


async def on_input_link(m: Message, widget: MessageInput, manager: DialogManager):
    downloader_controller: DownloaderController = manager.middleware_data['downloader_controller']
    user_id = manager.middleware_data['user_id']
    content_type = manager.dialog_data['selected_content_type']
    await manager.done()

    try:
        req_id = await downloader_controller.request_download(user_id, m, content_type)

        await manager.start(ProgressObserverDialogSG.main,
                            data={'req_id': req_id, 'req_msg': m},
                            mode=StartMode.NEW_STACK)
    except DayLimitException as ex:
        await m.answer(f'Превышен дневной лимит на скачивание!\nВам доступно: {ex.limit} за день')
    except ParallelLimitException as ex:
        await m.answer(f'Превышен лимит на одновременное скачивание!\nВам доступно: {ex.limit} за раз')
    except ContentDownloaderException as ex:
        await m.answer(get_err_msg(to_fail_status(ex)))
    except SameReqException as ex:
        await m.answer(f'Найден файл по вашему запросу. Скачивание доступно в течение суток от '
                       f'{ex.req.created_date}',
                       reply_markup=build_download_keyboard(ex.req))


async def on_site_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, item: str):
    photo_support, video_support = get_supported_sites()[item]
    manager.dialog_data['photo_support'] = photo_support
    manager.dialog_data['video_support'] = video_support
    manager.dialog_data['selected_site'] = item

    await manager.switch_to(MainDialogSG.content_type_select)


async def on_content_type_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, item: str):
    manager.dialog_data['selected_content_type'] = get_content_types()[item]
    await manager.switch_to(MainDialogSG.download_link_input)


async def sites_getter(**kwargs):
    return {
        'sites': list(map(lambda c: [c], get_supported_sites().keys()))
    }


async def content_types_getter(**kwargs):
    site = kwargs['dialog_manager'].dialog_data['selected_site']
    supported_types_bool = get_supported_sites()[site]
    supported_types = []

    for type_name, is_supported in zip(get_content_types(), supported_types_bool):
        if is_supported:
            supported_types.append(type_name)

    return {
        'content_types': list(map(lambda c: [c], supported_types))
    }


async def run_pre_dialogs(manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']

    if not await user_controller.is_subscribed(manager):
        await manager.start(SubAlertDialogSG.warn_text, show_mode=ShowMode.SEND)

    elif not user_controller.are_rules_accepted(manager):
        await manager.event.bot.send_message(manager.event.from_user.id, '‼️ Включите уведомления, чтобы мы смогли '
                                                                         'вовремя сообщить о новостях и '
                                                                         'поделиться другой важной информацией.')
        await asyncio.sleep(2)
        await manager.start(RulesAgreementDialogSG.main, show_mode=ShowMode.SEND)


async def on_process_result(start_data: dict, result: Any, dialog_manager: DialogManager):
    await run_pre_dialogs(dialog_manager)


async def on_dialog_start(start_data: dict, manager: DialogManager):
    await run_pre_dialogs(manager)


main_dialog = Dialog(
    Window(

        Const('''Инструкция пользования YOLICO ботом

Для отправки бесплатных запросов:

 ⬛  <strong>За один раз можно отправить только одну ссылку на фото/видео, которое хотите обработать;</strong>

 ⬛  <strong>Отправлять только ссылки, без постороннего текста;</strong>

 ⬛  <strong>Лимит бесплатных генераций в YOLICO боте медиаматериалов не более 5 ссылок в сутки;</strong>

Выберите сайт из доступного списка с кнопками 👇'''),

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
        Const('Доступные форматы'),
        Group(
            Select(
                Format('{item[0]}'),
                id='content_type_list',
                item_id_getter=operator.itemgetter(0),
                items='content_types',
                on_click=on_content_type_selected
            ),
            width=2
        ),
        Back(Const('◀ Назад')),
        state=MainDialogSG.content_type_select,
        getter=content_types_getter
    ),
    Window(
        Const('Введите ссылку на медиаматериал:'),
        MessageInput(on_input_link),
        state=MainDialogSG.download_link_input
    ),
    on_start=on_dialog_start,
    on_process_result=on_process_result
)
