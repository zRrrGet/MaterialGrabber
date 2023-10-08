from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.req_handler import ParallelLimitException


class ParallelLimitHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        limit = 2
        if len(request.request_repo.get_user_unfinished_requests(request.req.user_id)) >= limit:
            raise ParallelLimitException(limit)
