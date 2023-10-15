from datetime import datetime, timezone, timedelta

from .day_limit_interactor import IDayLimitInteractor
from .requests_limit import DayRequestsLimit
from ...repositories.download_request_repo import IDownloadRequestRepository


class DayLimitInteractor(IDayLimitInteractor):

    def __init__(self, request_repo: IDownloadRequestRepository):
        self.request_repo = request_repo

    def get_limit(self, user_id: int) -> DayRequestsLimit:
        base_day_limit = 5

        requests = self.request_repo.get_user_requests_this_day(user_id)
        is_request_allowed = len(requests) < base_day_limit
        left_requests = base_day_limit - len(requests)
        next_request_time = None

        if requests:
            next_request_time = requests[0].created_date + timedelta(days=1)

        return DayRequestsLimit(base_day_limit, is_request_allowed, left_requests, next_request_time)
