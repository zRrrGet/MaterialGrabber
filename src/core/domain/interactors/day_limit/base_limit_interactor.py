from datetime import timedelta

from .day_limit_interactor import IDayLimitInteractor
from .requests_limit import DayRequestsLimit
from ...entities.download_request import FailStatus, RequestStatus

from ...repositories.download_request_repo import IDownloadRequestRepository
from ...repositories.user_repo import IUserRepository


class DayLimitInteractor(IDayLimitInteractor):

    def __init__(self, request_repo: IDownloadRequestRepository, user_repo: IUserRepository):
        self.request_repo = request_repo
        self.user_repo = user_repo

    def get_limit(self, user_id: int) -> DayRequestsLimit:
        if self.user_repo.get_user(user_id).has_req_limit:
            return DayRequestsLimit(-1, True, -1, None)

        base_day_limit = 5

        requests = self.request_repo.get_user_requests_this_day(user_id)
        done_requests = list(filter(lambda x: (x.fail_status == FailStatus.no_exception and
                                               x.status == RequestStatus.finished), requests))

        is_request_allowed = len(done_requests) < base_day_limit
        left_requests = base_day_limit - len(done_requests)
        next_request_time = None

        if done_requests:
            next_request_time = done_requests[0].created_date + timedelta(days=1)

        return DayRequestsLimit(base_day_limit, is_request_allowed, left_requests, next_request_time)
