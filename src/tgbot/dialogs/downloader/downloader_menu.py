import operator
from typing import Any

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Group, Select, Back, Cancel
from aiogram_dialog.widgets.input import MessageInput

from src.tgbot.dialogs.progress.progress_observer import get_err_msg, build_download_keyboard
from src.tgbot.dialogs.back_msg import answer_back_msg

from src.tgbot.misc.states import DownloaderDialogSG, SubAlertDialogSG, RulesAgreementDialogSG, ProgressObserverDialogSG

from src.core.external.controllers.user_controller import UserController
from src.core.external.controllers.downloader_controller import DownloaderController

from src.core.domain.entities.download_request import ContentType
from src.core.domain.exceptions.req_handler import *
from src.core.domain.exceptions.downloader import *

from .content_stocks import ContentStock, get_stock_titles, get_content_stock


async def on_input_link(m: Message, widget: MessageInput, manager: DialogManager):
    downloader_controller: DownloaderController = manager.middleware_data['downloader_controller']
    user_id = manager.middleware_data['user_id']
    content_type = manager.dialog_data['selected_content_type']
    await manager.reset_stack()

    try:
        req_id = await downloader_controller.request_download(user_id, m, content_type)

        await manager.start(ProgressObserverDialogSG.main,
                            data={'req_id': req_id, 'req_msg': m},
                            mode=StartMode.NEW_STACK)
    except SubValidationException:
        await manager.start(SubAlertDialogSG.warn_text, show_mode=ShowMode.SEND)
    except DayLimitException as ex:
        await answer_back_msg(m, f'Превышен дневной лимит на генерацию!\n'
                                 f'Вам доступно: {ex.day_req_limit.day_limit} за день.\n'
                                 f'Следующая генерация будет доступна: '
                                 f'{ex.day_req_limit.next_request_time.strftime("%d-%m-%Y %H:%M:%S")}')
    except ParallelLimitException as ex:
        await answer_back_msg(m, f'Превышен лимит на одновременную генерацию!\nВам доступно: {ex.limit} за раз')
    except ContentDownloaderException as ex:
        await answer_back_msg(m, get_err_msg(to_fail_status(ex)))
    except SameReqException as ex:
        await answer_back_msg(m, f'Найден файл по вашему запросу. Скачивание доступно в течение суток от '
                                 f'{ex.req.created_date.strftime("%d-%m-%Y %H:%M:%S")}',
                                 build_download_keyboard(ex.req))


async def on_stock_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, stock_title: str):
    manager.dialog_data['selected_stock'] = get_content_stock(stock_title)
    await manager.switch_to(DownloaderDialogSG.content_type_select)


async def on_content_type_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, type_value: str):
    manager.dialog_data['selected_content_type'] = ContentType(int(type_value))
    await manager.switch_to(DownloaderDialogSG.download_link_input)


async def stocks_getter(**kwargs):
    return {
        'stocks': get_stock_titles()
    }


async def content_types_getter(dialog_manager: DialogManager, **kwargs):
    stock: ContentStock = dialog_manager.dialog_data['selected_stock']

    return {
        'content_types': stock.content_type_titles
    }


async def stock_link_getter(dialog_manager: DialogManager, **kwargs):
    stock: ContentStock = dialog_manager.dialog_data['selected_stock']

    return {
        'stock_link': stock.html_link
    }


downloader_dialog = Dialog(
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
                id='stock_list',
                item_id_getter=operator.itemgetter(0),
                items='stocks',
                on_click=on_stock_selected
            ),
            width=2
        ),

        Cancel(Const('◀ Назад')),
        state=DownloaderDialogSG.main,
        getter=stocks_getter
    ),
    Window(
        Const('Доступные форматы'),
        Group(
            Select(
                Format('{item[0]}'),
                id='content_type_list',
                item_id_getter=operator.itemgetter(1),
                items='content_types',
                on_click=on_content_type_selected
            ),
            width=2
        ),
        Back(Const('◀ Назад')),
        state=DownloaderDialogSG.content_type_select,
        getter=content_types_getter
    ),
    Window(
        Format('Отправьте ссылку на медиафайл с {stock_link}'),
        Back(Const('◀ Назад')),
        MessageInput(on_input_link),
        state=DownloaderDialogSG.download_link_input,
        getter=stock_link_getter
    )
)
