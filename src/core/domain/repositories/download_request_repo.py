from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.download_request import DownloadRequest
from src.core.domain.entities.download_request import RequestStatus, FailStatus


class IDownloadRequestRepository(ABC):

    @abstractmethod
    def add_request(self, request: DownloadRequest) -> int:
        pass

    @abstractmethod
    def get_request(self, request_id: int) -> Optional[DownloadRequest]:
        pass

    @abstractmethod
    def get_unfinished_requests(self) -> list[DownloadRequest]:
        pass

    @abstractmethod
    def get_user_requests_this_day(self, user_id: int) -> list[DownloadRequest]:
        pass

    @abstractmethod
    def get_user_unfinished_requests(self, user_id: int) -> list[DownloadRequest]:
        pass

    @abstractmethod
    def get_requests_by_url(self, download_url: str) -> list[DownloadRequest]:
        pass

    @abstractmethod
    def update_status(self, request_id: int, status: RequestStatus):
        pass

    @abstractmethod
    def update_fail_status(self, request_id: int, fail_status: FailStatus):
        pass

    @abstractmethod
    def update_content_link(self, request_id: int, content_link: str):
        pass
