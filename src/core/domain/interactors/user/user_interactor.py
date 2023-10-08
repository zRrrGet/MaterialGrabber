from abc import ABC, abstractmethod
from src.core.domain.entities.channel import Channel


class IUserInteractor(ABC):

    @abstractmethod
    def ensure_user(self, tg_id: int) -> int:
        pass

    @abstractmethod
    async def get_unsubscribed_channels(self, user_id: int) -> list[Channel]:
        pass

    @abstractmethod
    def are_rules_accepted(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def update_rules_agreement(self, user_id: int, agreed_with_rules: bool):
        pass
