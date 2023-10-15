from src.core.domain.interactors.day_limit.requests_limit import DayRequestsLimit
from src.core.domain.entities.download_request import DownloadRequest
from src.core.domain.exceptions import MaterialGrabberException


class ReqHandlerException(MaterialGrabberException):
    pass


class SubValidationException(ReqHandlerException):
    pass


class ParallelLimitException(ReqHandlerException):
    def __init__(self, limit: int):
        self.limit = limit


class DayLimitException(ReqHandlerException):
    def __init__(self, day_req_limit: DayRequestsLimit):
        self.day_req_limit = day_req_limit


class SameReqException(ReqHandlerException):
    def __init__(self, req: DownloadRequest):
        self.req = req
