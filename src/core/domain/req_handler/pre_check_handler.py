from requests import Session

from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler

from src.core.external.components.content_downloader.sources.downloader_client_factory import DownloaderClientFactory


class PreCheckHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        DownloaderClientFactory.create(request.req.download_link, request.req.content_type, Session())
