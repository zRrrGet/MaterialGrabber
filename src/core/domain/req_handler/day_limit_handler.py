from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.req_handler import DayLimitException


class DayLimitHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        limit = 7
        if len(request.request_repo.get_user_requests_this_day(request.req.user_id)) >= limit:
            raise DayLimitException(limit)
