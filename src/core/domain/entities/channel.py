from typing import Optional, Union
from dataclasses import dataclass


@dataclass
class Channel(object):
    id: Optional[int]
    chat_id: Union[int, str]
    join_link: str
