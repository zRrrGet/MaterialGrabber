from .downloader_client import IDownloaderClient
from src.core.external.components.content_downloader.link_parser.link_parser import ILinkParser


class DepositphotosClient(IDownloaderClient):

    def __init__(self, link_parser: ILinkParser):
        super().__init__(link_parser)
        self.session.headers.update({'Origin': 'https://toolxox.com',
                                     'Referer': 'https://toolxox.com'})

    @property
    def endpoint(self) -> str:
        return 'https://toolxox.com/dl/2/dp_img2/getwx.php'

    @staticmethod
    def prepare_request_link(link: str) -> str:
        content_id = link.split('-')[-1].replace('.html', '')
        return f'https://depositphotos.com/{content_id}'

    def get_download_links(self, link: str) -> list[str]:
        data = {
            'get_url': self.prepare_request_link(link),
            'download': ''
        }

        response = self.session.post(url=self.endpoint, data=data)
        return self.link_parser.parse(response.text)
