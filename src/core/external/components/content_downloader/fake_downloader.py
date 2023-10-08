import sys
import os
import uuid

from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.entities.download_request import ContentType


class FakeContentDownloader(IContentDownloader):

    def download(self, link: str, content_type: ContentType) -> str:
        local_filename = f'{sys.path[0]}\\data\\{str(uuid.uuid4())}.jpg'
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)
        with open(local_filename, 'wb') as f:
            return local_filename
