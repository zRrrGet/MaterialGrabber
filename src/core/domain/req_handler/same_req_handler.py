from datetime import datetime, timezone, timedelta

from .abstract_handler import HandlerRequest
from .abstract_handler import AbstractHandler
from src.core.domain.exceptions.req_handler import SameReqException


class SameReqHandler(AbstractHandler):

    async def process_request(self, request: HandlerRequest):
        same_link_requests = request.request_repo.get_requests_by_url(request.req.download_link)
        if same_link_requests:
            last_req = same_link_requests[-1]

            current_time = datetime.now(timezone.utc)
            day_ago = current_time - timedelta(days=1)

            if last_req.created_date > day_ago and last_req.content_link:
                raise SameReqException(last_req)
