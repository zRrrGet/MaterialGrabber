from typing import BinaryIO

from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.entities.download_request import ContentType


class FakeContentDownloader(IContentDownloader):

    def download(self, link: str, content_type: ContentType) -> BinaryIO:
        with open('file2.bin', 'wb') as f:
            return f
