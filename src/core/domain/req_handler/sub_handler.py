from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.req_handler import SubValidationException


class SubHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        if await request.user_interactor.get_unsubscribed_channels(request.req.user_id):
            raise SubValidationException()
