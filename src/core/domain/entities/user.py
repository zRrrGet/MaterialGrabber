from dataclasses import dataclass


@dataclass
class User(object):
    id: int
    tg_id: int
    subscribed_on_channels: bool
