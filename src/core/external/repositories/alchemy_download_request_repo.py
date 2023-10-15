from typing import Optional
import datetime

from sqlalchemy import update

from .alchemy_base import AlchemyBaseRepo
from src.core.external.orm.models import DownloadRequest
from src.core.domain.entities.download_request import DownloadRequest as EntityDownloadRequest
from src.core.domain.entities.download_request import RequestStatus, FailStatus
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository

from src.core.external.orm.mappers.download_request_mapper import DownloadRequestMapper


class AlchemyDownloadRequestRepo(IDownloadRequestRepository, AlchemyBaseRepo):

    def add_request(self, request: EntityDownloadRequest) -> int:
        session = self.session()
        new_request = DownloadRequestMapper.to_model(request)

        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        session.close()

        return new_request.id

    def get_request(self, request_id: int) -> Optional[EntityDownloadRequest]:
        session = self.session()
        req = session.get(DownloadRequest, request_id)
        if not req:
            return None

        session.close()
        return DownloadRequestMapper.to_entity(req)

    def filter(self, *criterion) -> list[EntityDownloadRequest]:
        session = self.session()
        requests = session.query(DownloadRequest).order_by(DownloadRequest.created_date).filter(*criterion).all()
        session.close()
        return list(map(lambda c: DownloadRequestMapper.to_entity(c), requests))

    def get_unfinished_requests(self) -> list[EntityDownloadRequest]:
        return self.filter(DownloadRequest.status != RequestStatus.finished)

    def get_user_requests_this_day(self, user_id: int) -> list[EntityDownloadRequest]:
        current_time = datetime.datetime.utcnow()
        day_ago = current_time - datetime.timedelta(days=1)
        return self.filter(DownloadRequest.created_date > day_ago,
                           DownloadRequest.user_id == user_id)

    def get_user_unfinished_requests(self, user_id: int) -> list[EntityDownloadRequest]:
        return self.filter(DownloadRequest.status != RequestStatus.finished,
                           DownloadRequest.user_id == user_id)

    def get_requests_by_url(self, download_url: str) -> list[EntityDownloadRequest]:
        return self.filter(DownloadRequest.download_link == download_url)

    def update_status(self, request_id: int, status: RequestStatus):
        self.execute(update(DownloadRequest).where(DownloadRequest.id == request_id).values({'status': status}))

    def update_fail_status(self, request_id: int, fail_status: FailStatus):
        self.execute(update(DownloadRequest).where(DownloadRequest.id == request_id)
                     .values({'fail_status': fail_status}))

    def update_content_link(self, request_id: int, content_link: str):
        self.execute(update(DownloadRequest).where(DownloadRequest.id == request_id)
                     .values({'content_link': content_link}))
