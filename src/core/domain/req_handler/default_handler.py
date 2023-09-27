from .abstract_handler import AbstractHandler


class DefaultHandler(AbstractHandler):
    async def process_request(self, request):
        return True
