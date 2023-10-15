from src.core.domain.interactors.day_limit.day_limit_interactor import IDayLimitInteractor
from src.core.domain.interactors.day_limit.requests_limit import DayRequestsLimit


class DayLimitController:

    def __init__(self, day_limit_interactor: IDayLimitInteractor):
        self.day_limit_interactor = day_limit_interactor

    def get_limit(self, user_id: int) -> DayRequestsLimit:
        return self.day_limit_interactor.get_limit(user_id)
