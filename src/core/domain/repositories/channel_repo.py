from abc import ABC, abstractmethod
from src.core.domain.entities.channel import Channel


class IChannelRepository(ABC):

    @abstractmethod
    def add_channel(self, channel: Channel):
        pass

    @abstractmethod
    def remove_channel(self, channel_id: int):
        pass

    @abstractmethod
    def get_channels(self) -> list[Channel]:
        pass
