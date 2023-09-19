from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_tg(self, tg_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def change_sub_by_tg(self, tg_id: int, subscribed: bool) -> Optional[User]:
        pass
