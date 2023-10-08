from bs4 import BeautifulSoup

from src.core.domain.exceptions.downloader import LinkPrepareException
from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class EnvatoClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/envato-photos-downloader.php'

    def prepare_request_link(self, link: str) -> str:
        try:
            resp = self.session.get(link)
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.find(class_='DBUVjoqm')['src']
        except (TypeError, KeyError):
            raise LinkPrepareException()
