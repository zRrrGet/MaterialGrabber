from abc import ABC, abstractmethod

from .user_repo import IUserRepository
from .channel_repo import IChannelRepository


class IRepositoryFactory(ABC):

    @abstractmethod
    def create_user_repo(self) -> IUserRepository:
        pass

    @abstractmethod
    def create_channel_repo(self) -> IChannelRepository:
        pass
