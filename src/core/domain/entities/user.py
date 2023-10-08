from typing import Optional
from dataclasses import dataclass


@dataclass
class User(object):
    id: Optional[int]
    tg_id: int
    subscribed_on_channels: bool
    accepted_rules: bool
