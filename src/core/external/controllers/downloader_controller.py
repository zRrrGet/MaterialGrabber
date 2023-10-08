from aiogram.types import Message

from src.core.domain.interactors.content_downloader.downloader_interactor import IDownloaderInteractor
from src.core.domain.entities.download_request import DownloadRequest, ContentType


class DownloaderController:

    def __init__(self, downloader_interactor: IDownloaderInteractor):
        self.downloader_interactor = downloader_interactor

    async def request_download(self, user_id: int, message: Message, content_type: ContentType) -> int:
        return await self.downloader_interactor.request_download(user_id, message.text, content_type)

    def get_request(self, request_id: int) -> DownloadRequest:
        return self.downloader_interactor.get_request(request_id)
