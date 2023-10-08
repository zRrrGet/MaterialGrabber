import datetime
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


class FailStatus(enum.Enum):
    no_exception = 0
    unexpected_ex = 1
    requests_ex = 2

    unsupported_domain = 3
    endpoint_parse_ex = 4
    link_prepare_ex = 5
    no_results_found = 6
    empty_file = 7

    file_storage_ex = 8


@dataclass
class DownloadRequest(object):
    id: Optional[int]
    user_id: int
    download_link: str
    content_link: str
    content_type: ContentType
    status: RequestStatus
    fail_status: FailStatus
    created_date: Optional[datetime.datetime]
