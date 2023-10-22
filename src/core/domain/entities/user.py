from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User(object):
    id: Optional[int]
    tg_id: int
    username: str
    full_name: str
    joined_date: Optional[datetime]
    subscribed_on_channels: bool
    accepted_rules: bool
    has_req_limit: bool
