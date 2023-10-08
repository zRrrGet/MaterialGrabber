from abc import ABC, abstractmethod
from requests import Session

from src.core.external.components.content_downloader.sources.link_parser.link_parser import ILinkParser


class IDownloaderClient(ABC):

    def __init__(self, link_parser: ILinkParser, session: Session):
        self.link_parser = link_parser
        self.session = session

    @abstractmethod
    def get_download_links(self, link: str) -> list[str]:
        pass
