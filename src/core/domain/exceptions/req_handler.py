from src.core.domain.entities.download_request import DownloadRequest
from src.core.domain.exceptions import MaterialGrabberException


class ReqHandlerException(MaterialGrabberException):
    pass


class SubValidationException(ReqHandlerException):
    pass


class LimitException(ReqHandlerException):
    def __init__(self, limit: int):
        self.limit = limit


class DayLimitException(LimitException):
    pass


class ParallelLimitException(LimitException):
    pass


class SameReqException(ReqHandlerException):
    def __init__(self, req: DownloadRequest):
        self.req = req
