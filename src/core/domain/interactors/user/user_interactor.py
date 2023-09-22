from abc import ABC, abstractmethod
from src.core.domain.entities.channel import Channel


class IUserInteractor(ABC):

    @abstractmethod
    def ensure_user(self, tg_id: int):
        pass

    @abstractmethod
    async def get_unsubscribed_channels(self, tg_id: int) -> list[Channel]:
        pass
