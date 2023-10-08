from requests import Session

from src.core.external.components.content_downloader.sources.base.toolxox import ToolxoxClient
from src.core.external.components.content_downloader.sources.link_parser.link_parser import ILinkParser


class EyeemClient(ToolxoxClient):

    def __init__(self, link_parser: ILinkParser, session: Session):
        super().__init__(link_parser, session)
        self.session.headers.update({'Referer': 'https://toolxox.com/dl/eyeem/index.php'})

    @property
    def endpoint(self) -> str:
        return 'https://toolxox.com/dl/eyeem/get2x.php'
