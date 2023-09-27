from abc import ABC, abstractmethod

from .user_repo import IUserRepository
from .channel_repo import IChannelRepository
from .download_request_repo import IDownloadRequestRepository


class IRepositoryFactory(ABC):

    @abstractmethod
    def create_user_repo(self) -> IUserRepository:
        pass

    @abstractmethod
    def create_channel_repo(self) -> IChannelRepository:
        pass

    @abstractmethod
    def create_download_request_repo(self) -> IDownloadRequestRepository:
        pass
