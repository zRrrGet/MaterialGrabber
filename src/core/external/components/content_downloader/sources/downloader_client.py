from abc import ABC, abstractmethod
import requests

from src.core.external.components.content_downloader.link_parser.link_parser import ILinkParser


class IDownloaderClient(ABC):

    def __init__(self, link_parser: ILinkParser):
        self.link_parser = link_parser

        self.session = requests.Session()
        self.session.headers.update(
            {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        )

    @abstractmethod
    def get_download_links(self, link: str) -> list[str]:
        pass
