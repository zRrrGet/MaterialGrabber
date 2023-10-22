from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def add_user(self, user: User) -> int:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_tg(self, tg_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def update_sub(self, user_id: int, subscribed: bool):
        pass

    @abstractmethod
    def update_rules_agreement(self, user_id: int, agreed_with_rules: bool):
        pass

    @abstractmethod
    def reset_sub_all(self):
        pass
