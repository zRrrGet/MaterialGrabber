from abc import ABC, abstractmethod
from src.core.domain.entities.download_request import DownloadRequest, ContentType


class IDownloaderInteractor(ABC):

    @abstractmethod
    async def request_download(self, user_id: int, download_link: str, content_type: ContentType) -> int:
        pass

    @abstractmethod
    def get_request(self, request_id: int) -> DownloadRequest:
        pass
