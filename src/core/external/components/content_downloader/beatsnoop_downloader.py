import os
import sys
import uuid
import requests
import magic
import mimetypes

from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.entities.download_request import ContentType
from src.core.domain.exceptions.downloader import *

from .sources.downloader_client_factory import DownloaderClientFactory
from .session_factory.session_factory import ISessionFactory


class BeatsnoopDownloader(IContentDownloader):

    def __init__(self, session_factory: ISessionFactory):
        self.session_factory = session_factory

    @staticmethod
    def download_file(url: str, session: requests.Session) -> str:
        with session.get(url, stream=True) as r:
            local_filename = f'{sys.path[0]}\\data\\{str(uuid.uuid4())}'

            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            if not os.stat(local_filename).st_size:
                os.remove(local_filename)
                raise EmptyFileException()

            ext = magic.from_file(local_filename, mime=True)
            file_ext = mimetypes.guess_extension(ext)
            final_filename = f'{local_filename}{file_ext}'
            os.rename(local_filename, final_filename)

        return final_filename

    def download(self, link: str, content_type: ContentType) -> str:
        session = self.session_factory.create()

        download_link_getter = DownloaderClientFactory.create(link, content_type, session)
        urls = download_link_getter.get_download_links(link)

        if not urls:
            raise NoResultsFoundException()

        for url in urls:
            try:
                return self.download_file(url, session)
            except (EmptyFileException, requests.exceptions.RequestException):
                if url == urls[-1]:
                    raise
