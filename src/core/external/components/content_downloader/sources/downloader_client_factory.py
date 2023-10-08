from urllib.parse import urlparse
from requests import Session

from src.core.domain.exceptions.downloader import *
from src.core.domain.entities.download_request import ContentType
from .downloader_client import IDownloaderClient

from src.core.external.components.content_downloader.sources.clients.depositphotos import DepositphotosClient
from src.core.external.components.content_downloader.sources.clients.envato import EnvatoClient
from src.core.external.components.content_downloader.sources.clients.istockphoto import IstockphotoClient
from src.core.external.components.content_downloader.sources.clients.istockvideo import IstockvideoClient
from src.core.external.components.content_downloader.sources.clients.gettyimages import GettyimagesClient
from src.core.external.components.content_downloader.sources.clients.gettyvideos import GettyvideosClient
from src.core.external.components.content_downloader.sources.clients.motionarray import MotionarrayClient
from src.core.external.components.content_downloader.sources.clients.shutterstock import ShutterstockClient
from src.core.external.components.content_downloader.sources.clients.storyblocks_video import StoryblocksVideoClient
from src.core.external.components.content_downloader.sources.clients.storyblocks_photo import StoryblocksPhotoClient
from src.core.external.components.content_downloader.sources.clients.videezy import VideezyClient
from src.core.external.components.content_downloader.sources.clients.eyeem import EyeemClient

from .link_parser.base_link_parser import BaseLinkParser
from .link_parser.raw_link_parser import RawLinkParser
from .link_parser.proxy_link_parser import ProxyLinkParser


class DownloaderClientFactory:

    @staticmethod
    def get_client(hostname: str, content_type: ContentType):
        return {
            'depositphotos.com': {
                content_type.photo: DepositphotosClient,
                content_type.video: DepositphotosClient
            },
            'elements.envato.com': {
                content_type.photo: EnvatoClient
            },
            'www.istockphoto.com': {
                content_type.photo: IstockphotoClient,
                content_type.video: IstockvideoClient
            },
            'www.gettyimages.com': {
                content_type.photo: GettyimagesClient,
                content_type.video: GettyvideosClient
            },
            'motionarray.com': {
                content_type.photo: MotionarrayClient
            },
            'www.shutterstock.com': {
                content_type.photo: ShutterstockClient
            },
            'www.storyblocks.com': {
                content_type.photo: StoryblocksPhotoClient,
                content_type.video: StoryblocksVideoClient
            },
            'www.videezy.com': {
                content_type.video: VideezyClient
            },
            'www.eyeem.com': {
                content_type.photo: EyeemClient
            }
        }[hostname][content_type]

    @staticmethod
    def create(url: str, content_type: ContentType, session: Session) -> IDownloaderClient:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        link_parsers = {
            EyeemClient: RawLinkParser('https://toolxox.com/dl/eyeem/'),
            StoryblocksPhotoClient: RawLinkParser('https://toolxox.com/dl/sb/cap/'),
            ShutterstockClient: ProxyLinkParser(session)
        }

        try:
            client = DownloaderClientFactory.get_client(hostname, content_type)
            link_parser = link_parsers.get(client, BaseLinkParser())

            return client(link_parser, session)
        except KeyError:
            raise UnsupportedDomainException()
