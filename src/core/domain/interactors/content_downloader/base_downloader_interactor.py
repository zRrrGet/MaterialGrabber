from .downloader_interactor import IDownloaderInteractor
from src.core.domain.interactors.user.user_interactor import IUserInteractor
from ..day_limit.day_limit_interactor import IDayLimitInteractor

from src.core.domain.entities.download_request import DownloadRequest, ContentType
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository
from src.core.domain.entities.download_request import RequestStatus, FailStatus

from src.core.domain.req_handler.chain_factory import ChainFactory
from src.core.domain.req_handler.abstract_handler import HandlerRequest


class DownloaderInteractor(IDownloaderInteractor):

    def __init__(self, user_interactor: IUserInteractor, day_limit_interactor: IDayLimitInteractor,
                 request_repo: IDownloadRequestRepository, chain_factory: ChainFactory):
        self.user_interactor = user_interactor
        self.day_limit_interactor = day_limit_interactor
        self.request_repo = request_repo
        self.chain_factory = chain_factory

    async def request_download(self, user_id: int, download_link: str, content_type: ContentType) -> int:
        req = DownloadRequest(None, user_id, download_link, '', content_type, RequestStatus.waiting_queue,
                              FailStatus.no_exception, None)

        # Handling request
        validation_chain = self.chain_factory.create()
        await validation_chain.handle(HandlerRequest(self.user_interactor, self.day_limit_interactor,
                                                     self.request_repo, req))

        # Adding request to queue
        return self.request_repo.add_request(req)

    def get_request(self, request_id: int) -> DownloadRequest:
        return self.request_repo.get_request(request_id)
