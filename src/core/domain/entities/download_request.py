from typing import Optional
from dataclasses import dataclass
import enum


class RequestStatus(enum.Enum):
    waiting_queue = 0
    downloading_content = 1
    uploading = 2
    finished = 3


class ContentType(enum.Enum):
    photo = 0
    video = 1


@dataclass
class DownloadRequest(object):
    id: Optional[int]
    user_id: int
    download_link: str
    content_link: str
    status: RequestStatus
