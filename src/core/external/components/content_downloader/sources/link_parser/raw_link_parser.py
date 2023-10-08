from .link_parser import ILinkParser
from bs4 import BeautifulSoup


class RawLinkParser(ILinkParser):

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def build_download_links(self, links: list[str]) -> list[str]:
        return list(map(lambda c: f'{self.endpoint}{c}', links))

    def parse(self, page: str) -> list[str]:
        soup = BeautifulSoup(page, 'html.parser')
        link_items = soup.findAll('img')

        image_lins = list(map(lambda x: x['src'], link_items))
        relative_links = list(filter(lambda x: x.count('img/'), image_lins))
        return self.build_download_links(relative_links)
