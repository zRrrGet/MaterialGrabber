from .link_parser import ILinkParser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class BaseLinkParser(ILinkParser):

    def extract_straight_link(self, url: str) -> str:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

        for param in params.values():
            if urlparse(param[0]).scheme:
                return self.extract_straight_link(param[0])

        return url

    def parse(self, page: str) -> list[str]:
        download_links = []
        soup = BeautifulSoup(page, 'html.parser')
        link_items = soup.findAll('a')

        for item in link_items:
            link = item['href']
            if link.count('http://') + link.count('https://') >= 2:
                download_links.append(self.extract_straight_link(link))

        return download_links
