from requests import Session

from src.core.external.components.content_downloader.sources.base.toolxox import ToolxoxClient
from src.core.external.components.content_downloader.sources.link_parser.link_parser import ILinkParser


class ShutterstockClient(ToolxoxClient):

    def __init__(self, link_parser: ILinkParser, session: Session):
        super().__init__(link_parser, session)
        self.session.headers.update({'Origin': 'https://snapwordz.com',
                                     'Referer': 'https://snapwordz.com'})

    @property
    def endpoint(self) -> str:
        return 'https://snapwordz.com/dl/ss/get_xox.php'
