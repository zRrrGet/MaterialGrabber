from typing import Optional
import datetime
from dataclasses import dataclass


@dataclass
class DayRequestsLimit:
    day_limit: int
    is_request_allowed: bool
    left_requests: int
    next_request_time: Optional[datetime.datetime]
