from urllib.parse import urlparse

from src.core.domain.entities.download_request import ContentType
from .downloader_client import IDownloaderClient

from .depositphotos import DepositphotosClient
from .depositphotos_video import DepositphotosVideoClient
from .envato import EnvatoClient
from .istockphoto import IstockphotoClient
from .istockphoto_video import IstockphotoVideoClient

from src.core.external.components.content_downloader.link_parser.base_link_parser import BaseLinkParser


class DownloaderClientFactory:

    @staticmethod
    def create(url: str, content_type: ContentType) -> IDownloaderClient:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        clients = {
            'depositphotos.com': {
                content_type.photo: DepositphotosClient,
                content_type.video: DepositphotosClient
            },
            'envato-shoebox-0.imgix.net': {
                content_type.photo: EnvatoClient
            },
            'www.istockphoto.com': {
                content_type.photo: IstockphotoClient,
                content_type.video: IstockphotoVideoClient
            },
        }

        return clients[hostname][content_type](BaseLinkParser())
