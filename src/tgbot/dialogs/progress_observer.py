import asyncio
from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Progress, Format

from src.tgbot.misc.states import ProgressObserverDialogSG
from src.core.domain.entities.download_request import RequestStatus
from src.core.external.controllers.downloader_controller import DownloaderController


def get_state_name(status: RequestStatus) -> str:
    return [
        'Ваш запрос в очереди, ожидайте...',
        'Скачивание материалов...',
        'Загрузка в облако...',
        'Завершено'
    ][status.value]


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
    await m.answer(f'Загрузка завершена! Файл: {req.content_link}')


async def get_progress_data(dialog_manager: DialogManager, downloader_controller: DownloaderController, **kwargs):
    if not dialog_manager.dialog_data.get('observer_launched', False):
        req_id = dialog_manager.start_data['req_id']
        message = dialog_manager.start_data['req_msg']

        dialog_manager.dialog_data['observer_launched'] = True
        asyncio.create_task(observe_req_status(message, dialog_manager.bg(), req_id, downloader_controller))

    return {
        'status': dialog_manager.dialog_data.get('status', get_state_name(RequestStatus.waiting_queue)),
        'progress': dialog_manager.dialog_data.get('progress', 0)
    }


progress_observer_dialog = Dialog(
    Window(
        Format('{status}'),
        Progress('progress', 10),
        getter=get_progress_data,
        state=ProgressObserverDialogSG.main,
    )
)
