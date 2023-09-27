from .abstract_handler import AbstractHandler
from .sub_handler import SubHandler
from .default_handler import DefaultHandler
from .day_limit_handler import DayLimitHandler
from .parallel_limit_handler import ParallelLimitHandler


class ChainFactory:

    def create(self) -> AbstractHandler:
        return SubHandler(DayLimitHandler(ParallelLimitHandler(DefaultHandler(None))))
