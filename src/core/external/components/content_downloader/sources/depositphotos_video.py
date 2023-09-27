from .downloader_client import IDownloaderClient


class DepositphotosVideoClient(IDownloaderClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/depositphotos-videos-downloader.php'

    def get_download_links(self, link: str) -> list[str]:
        data = {
            'url': link,
            'token': '5f1c6979a54c99e1398296826675621a',
            'send': ''
        }

        response = self.session.post(url=self.endpoint, data=data)
        return self.link_parser.parse(response.text)
