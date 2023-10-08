from .abstract_handler import AbstractHandler
from .sub_handler import SubHandler
from .default_handler import DefaultHandler
from .day_limit_handler import DayLimitHandler
from .parallel_limit_handler import ParallelLimitHandler
from .same_req_handler import SameReqHandler
from .pre_check_handler import PreCheckHandler


class ChainFactory:

    def create(self) -> AbstractHandler:
        return PreCheckHandler(SubHandler(SameReqHandler(DayLimitHandler(ParallelLimitHandler(DefaultHandler(None))))))
