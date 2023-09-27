import datetime

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import update

from src.core.external.orm.models import DownloadRequest
from src.core.domain.entities.download_request import DownloadRequest as EntityDownloadRequest, RequestStatus
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository


class SqliteDownloadRequestRepo(IDownloadRequestRepository):

    def __init__(self, session: scoped_session):
        self.session = session

    def add_request(self, request: EntityDownloadRequest) -> int:
        session = self.session()
        new_request = DownloadRequest(id=request.id, user_id=request.user_id, download_link=request.download_link,
                                      content_link=request.content_link, status=request.status)
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        session.close()

        return new_request.id

    def get_request(self, request_id: int) -> EntityDownloadRequest:
        session = self.session()
        req = session.get(DownloadRequest, request_id)
        session.close()
        return EntityDownloadRequest(id=req.id, user_id=req.user_id, download_link=req.download_link,
                                     content_link=req.content_link, status=req.status)

    def get_unfinished_requests(self) -> list[EntityDownloadRequest]:
        session = self.session()
        requests = session.query(DownloadRequest).filter(DownloadRequest.status != RequestStatus.finished).all()
        session.close()
        return list(map(lambda c: EntityDownloadRequest(id=c.id,
                                                        user_id=c.user_id,
                                                        download_link=c.download_link,
                                                        content_link=c.content_link,
                                                        status=c.status), requests))

    def get_user_requests_this_day(self, user_id: int) -> list[DownloadRequest]:
        session = self.session()

        current_time = datetime.datetime.utcnow()
        day_ago = current_time - datetime.timedelta(days=1)

        requests = session.query(DownloadRequest).filter(DownloadRequest.created_date > day_ago,
                                                         DownloadRequest.user_id == user_id).all()
        session.close()
        return list(map(lambda c: EntityDownloadRequest(id=c.id,
                                                        user_id=c.user_id,
                                                        download_link=c.download_link,
                                                        content_link=c.content_link,
                                                        status=c.status), requests))

    def get_user_unfinished_requests(self, user_id: int) -> list[DownloadRequest]:
        session = self.session()
        requests = session.query(DownloadRequest).filter(DownloadRequest.status != RequestStatus.finished,
                                                         DownloadRequest.user_id == user_id).all()
        session.close()
        return list(map(lambda c: EntityDownloadRequest(id=c.id,
                                                        user_id=c.user_id,
                                                        download_link=c.download_link,
                                                        content_link=c.content_link,
                                                        status=c.status), requests))

    def update_status(self, request_id: int, status: RequestStatus):
        session = self.session()
        session.execute(update(DownloadRequest).where(DownloadRequest.id == request_id).values({'status': status}))
        session.commit()
        session.close()

    def update_content_link(self, request_id: int, content_link: str):
        session = self.session()
        session.execute(update(DownloadRequest).where(DownloadRequest.id == request_id)
                        .values({'content_link': content_link}))
        session.commit()
        session.close()
