from abc import ABC, abstractmethod


class ILinkParser(ABC):

    @abstractmethod
    def parse(self, page: str) -> list[str]:
        pass
