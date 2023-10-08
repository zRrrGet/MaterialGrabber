from abc import ABC, abstractmethod
from requests import Session


class ISessionFactory(ABC):

    @abstractmethod
    def create(self) -> Session:
        pass
