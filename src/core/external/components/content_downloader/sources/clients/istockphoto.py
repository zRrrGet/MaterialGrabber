from bs4 import BeautifulSoup

from src.core.domain.exceptions.downloader import EndpointParseException
from src.core.external.components.content_downloader.sources.base.toolxox import ToolxoxClient


class IstockphotoClient(ToolxoxClient):

    @property
    def endpoint_temp_root(self) -> str:
        return 'https://toolxox.com/dl/1/is_1.0/'

    @property
    def endpoint(self) -> str:
        try:
            resp = self.session.get(self.endpoint_temp_root)
            soup = BeautifulSoup(resp.text, 'html.parser')

            action = soup.find(id='rip-form')['action'].replace('\n', '')
            return f'{self.endpoint_temp_root}{action}'
        except (TypeError, KeyError):
            raise EndpointParseException()
