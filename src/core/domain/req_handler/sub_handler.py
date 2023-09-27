from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.handler_req_ex import SubValidationException


class SubHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        if await request.user_interactor.get_unsubscribed_channels(request.user_id):
            raise SubValidationException()
