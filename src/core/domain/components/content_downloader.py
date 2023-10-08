from abc import ABC, abstractmethod
from src.core.domain.entities.download_request import ContentType


class IContentDownloader(ABC):

    @abstractmethod
    def download(self, link: str, content_type: ContentType) -> str:
        pass
