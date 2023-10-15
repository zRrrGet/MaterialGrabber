from abc import ABC, abstractmethod
from .requests_limit import DayRequestsLimit


class IDayLimitInteractor(ABC):

    @abstractmethod
    def get_limit(self, user_id: int) -> DayRequestsLimit:
        pass
