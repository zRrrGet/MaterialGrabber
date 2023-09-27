from .downloader_interactor import IDownloaderInteractor
from src.core.domain.interactors.user.user_interactor import IUserInteractor
from src.core.domain.entities.download_request import DownloadRequest
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository
from src.core.domain.entities.download_request import RequestStatus

from src.core.domain.req_handler.chain_factory import ChainFactory
from src.core.domain.req_handler.abstract_handler import HandlerRequest


class DownloaderInteractor(IDownloaderInteractor):

    def __init__(self, user_interactor: IUserInteractor,
                 request_repo: IDownloadRequestRepository, chain_factory: ChainFactory):
        self.user_interactor = user_interactor
        self.request_repo = request_repo
        self.chain_factory = chain_factory

    async def request_download(self, user_id: int, download_link: str) -> int:
        validation_chain = self.chain_factory.create()
        await validation_chain.handle(HandlerRequest(self.user_interactor, self.request_repo, user_id))

        req = DownloadRequest(None, user_id, download_link, '', RequestStatus.waiting_queue)
        return self.request_repo.add_request(req)

    def get_request(self, request_id: int) -> DownloadRequest:
        return self.request_repo.get_request(request_id)
