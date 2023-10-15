import asyncio

from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_dialog import DialogManager
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Progress, Format

from src.tgbot.misc.states import ProgressObserverDialogSG
from src.core.domain.entities.download_request import RequestStatus, FailStatus, DownloadRequest
from src.core.external.controllers.downloader_controller import DownloaderController

from src.tgbot.dialogs.back_msg import answer_back_msg


def get_state_name(status: RequestStatus) -> str:
    return {
        status.waiting_queue: 'Ваш запрос в очереди, ожидайте...',
        status.downloading_content: 'Скачивание материалов...',
        status.uploading: 'Загрузка в облако...',
        status.finished: 'Завершено'
    }.get(status, 'Неизвестный статус')


def get_err_msg(status: FailStatus) -> str:
    return {
        status.unsupported_domain: 'Ошибка: указанный ресурс или формат контента для него не поддерживается',
        status.requests_ex: 'Ошибка: не удалось скачать файл. Проверьте правильность '
                            'адреса и повторите запрос',
        status.link_prepare_ex: 'Ошибка: не удалось получить нужную информацию о данной ссылке. Проверьте правильность '
                                'адреса и повторите запрос',
        status.no_results_found: 'Ошибка: ничего не найдено. Проверьте правильность '
                                 'адреса и повторите запрос',
        status.empty_file: 'Ошибка: не удалось скачать файл. Проверьте правильность '
                           'адреса и повторите запрос'
    }.get(status, 'Что-то пошло не так... К сожалению, нам не удалось загрузить файл :(\n'
                  'Попробуйте снова через некоторое время')


def build_download_keyboard(req: DownloadRequest) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Скачать', url=req.content_link),
         InlineKeyboardButton(text='Перейти на страницу', url=req.download_link)],
    ])


async def observe_req_status(m: Message, manager: DialogManager, request_id,
                             downloader_controller: DownloaderController):
    last_status = RequestStatus.waiting_queue
    while True:
        req = downloader_controller.get_request(request_id)

        if req.status != last_status:
            await manager.update({
                'status': get_state_name(req.status),
                'progress': req.status.value * 100 / 3,
            })
            last_status = req.status

        if req.status == RequestStatus.finished:
            break

        await asyncio.sleep(1)

    await manager.done()

    if req.fail_status == FailStatus.no_exception:
        keyboard = build_download_keyboard(req)
        await answer_back_msg(m, f'Загрузка завершена! Файл доступен для скачивания 24 часа.', keyboard)
    else:
        await answer_back_msg(m, get_err_msg(req.fail_status))


async def get_progress_data(dialog_manager: DialogManager, **kwargs):
    return {
        'status': dialog_manager.dialog_data.get('status', get_state_name(RequestStatus.waiting_queue)),
        'progress': dialog_manager.dialog_data.get('progress', 0)
    }


async def on_dialog_start(start_data: dict, manager: DialogManager):
    downloader_controller = manager.middleware_data['downloader_controller']
    req_id = start_data['req_id']
    message = start_data['req_msg']
    asyncio.create_task(observe_req_status(message, manager.bg(), req_id, downloader_controller))


progress_observer_dialog = Dialog(
    Window(
        Format('{status}'),
        Progress('progress', 10),
        getter=get_progress_data,
        state=ProgressObserverDialogSG.main,
    ),
    on_start=on_dialog_start
)
