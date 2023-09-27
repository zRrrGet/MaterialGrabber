import asyncio

from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository
from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.entities.download_request import RequestStatus, ContentType


class DownloaderWorker:

    def __init__(self, request_repo: IDownloadRequestRepository, content_downloader: IContentDownloader):
        self.request_repo = request_repo
        self.content_downloader = content_downloader

    def start(self):
        asyncio.ensure_future(self.download_loop())

    async def download_loop(self):
        while True:
            await self.download_routine()
            await asyncio.sleep(1)

    async def download_routine(self):
        for req in self.request_repo.get_unfinished_requests():
            self.request_repo.update_status(req.id, RequestStatus.downloading_content)

            file = self.content_downloader.download('sas', ContentType.photo)
            print(file.name)

            await asyncio.sleep(3)
            self.request_repo.update_status(req.id, RequestStatus.uploading)
            await asyncio.sleep(3)

            self.request_repo.update_content_link(req.id, 'https://google.com')
            self.request_repo.update_status(req.id, RequestStatus.finished)
