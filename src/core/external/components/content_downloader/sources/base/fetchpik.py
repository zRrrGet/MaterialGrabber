from src.core.external.components.content_downloader.sources.downloader_client import IDownloaderClient


class FetchpikClient(IDownloaderClient):

    @property
    def endpoint(self) -> str:
        raise RuntimeError('Not implemented')

    def prepare_request_link(self, link: str) -> str:
        return link

    def get_download_links(self, link: str) -> list[str]:
        data = {
            'url': self.prepare_request_link(link),
            'token': '5f1c6979a54c99e1398296826675621a',
            'send': ''
        }

        response = self.session.post(url=self.endpoint, data=data)
        return self.link_parser.parse(response.text)
