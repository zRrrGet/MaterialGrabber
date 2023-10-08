from src.core.domain.exceptions.downloader import LinkPrepareException
from src.core.external.components.content_downloader.sources.base.toolxox import ToolxoxClient


class DepositphotosClient(ToolxoxClient):

    @property
    def endpoint(self) -> str:
        return 'https://toolxox.com/dl/2/dp_img2/getwx.php'

    def prepare_request_link(self, link: str) -> str:
        try:
            content_id = link.split('?')[0].split('-')[-1].replace('.html', '')
            return f'https://depositphotos.com/{content_id}'
        except IndexError:
            raise LinkPrepareException()
