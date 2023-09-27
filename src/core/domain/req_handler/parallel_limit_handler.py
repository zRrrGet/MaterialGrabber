from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.handler_req_ex import ParallelLimitException


class ParallelLimitHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        limit = 2
        if len(request.request_repo.get_user_unfinished_requests(request.user_id)) >= limit:
            raise ParallelLimitException(limit)
