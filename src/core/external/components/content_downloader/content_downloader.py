import os
import uuid
import requests
import magic
import mimetypes

from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.entities.download_request import ContentType

from .sources.downloader_client_factory import DownloaderClientFactory


class ContentDownloader(IContentDownloader):

    @staticmethod
    def download_file(url) -> str:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            local_filename = str(uuid.uuid4())

            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            if not os.stat(local_filename).st_size:
                raise RuntimeError('Empty file')

            ext = magic.from_file(local_filename, mime=True)
            file_ext = mimetypes.guess_extension(ext)
            final_filename = f'{local_filename}{file_ext}'
            os.rename(local_filename, final_filename)

        return final_filename

    def download(self, link: str, content_type: ContentType) -> str:
        download_link_getter = DownloaderClientFactory.create(link, content_type)
        url = download_link_getter.get_download_links(link)
        return self.download_file(url)
