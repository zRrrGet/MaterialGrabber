from requests import Session
from .base_link_parser import BaseLinkParser
from bs4 import BeautifulSoup


class ProxyLinkParser(BaseLinkParser):

    def __init__(self, session: Session):
        self.session = session

    def parse(self, page: str) -> list[str]:
        download_urls = super().parse(page)
        handled_links = []

        for url in download_urls:
            resp = self.session.get(url)
            content_type = resp.headers['content-type']
            if content_type.count('text/html'):
                soup = BeautifulSoup(resp.text, 'html.parser')
                handled_links.append(soup.find('a')['href'])
            else:
                handled_links.append(url)

        return handled_links
