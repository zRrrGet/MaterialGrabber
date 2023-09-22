from abc import ABC, abstractmethod
from typing import Union


class ISubValidator(ABC):

    @abstractmethod
    def validate(self, chat_id: Union[int, str], user_id: int) -> bool:
        pass
