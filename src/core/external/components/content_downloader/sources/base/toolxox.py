from requests import Session

from src.core.external.components.content_downloader.sources.downloader_client import IDownloaderClient
from src.core.external.components.content_downloader.sources.link_parser.link_parser import ILinkParser


class ToolxoxClient(IDownloaderClient):

    def __init__(self, link_parser: ILinkParser, session: Session):
        super().__init__(link_parser, session)
        self.session.headers.update({'Origin': 'https://toolxox.com',
                                     'Referer': 'https://toolxox.com'})

    @property
    def endpoint(self) -> str:
        raise RuntimeError('Not implemented')

    def prepare_request_link(self, link: str) -> str:
        return link

    def get_download_links(self, link: str) -> list[str]:
        data = {
            'get_url': self.prepare_request_link(link),
            'download': ''
        }

        response = self.session.post(url=self.endpoint, data=data)
        return self.link_parser.parse(response.text)
