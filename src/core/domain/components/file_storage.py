from abc import ABC, abstractmethod


class IFileStorage(ABC):

    @abstractmethod
    def upload(self, file_path: str) -> str:
        pass
