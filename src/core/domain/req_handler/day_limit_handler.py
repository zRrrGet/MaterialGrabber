from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.req_handler import DayLimitException


class DayLimitHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        day_req_limit = request.day_limit_interactor.get_limit(request.req.user_id)
        if not day_req_limit.is_request_allowed:
            raise DayLimitException(day_req_limit)
