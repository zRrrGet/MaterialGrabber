from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.domain.interactors.user.user_interactor import IUserInteractor
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository


@dataclass
class HandlerRequest:
    user_interactor: IUserInteractor
    request_repo: IDownloadRequestRepository
    user_id: int


class AbstractHandler(ABC):

    def __init__(self, nxt):
        self._nxt = nxt

    async def handle(self, request: HandlerRequest):
        handled = await self.process_request(request)

        if not handled:
            await self._nxt.handle(request)

    @abstractmethod
    async def process_request(self, request: HandlerRequest):
        pass
