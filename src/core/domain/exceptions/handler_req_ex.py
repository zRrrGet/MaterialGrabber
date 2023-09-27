from src.core.domain.exceptions import MaterialGrabberException


class SubValidationException(MaterialGrabberException):
    pass


class LimitException(MaterialGrabberException):
    def __init__(self, limit: int):
        self.limit = limit


class DayLimitException(LimitException):
    pass


class ParallelLimitException(LimitException):
    pass
