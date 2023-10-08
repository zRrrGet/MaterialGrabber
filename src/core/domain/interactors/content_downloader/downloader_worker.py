import concurrent.futures
import logging
import os
import threading
import time

import requests

from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository
from src.core.domain.components.content_downloader import IContentDownloader
from src.core.domain.components.file_storage import IFileStorage
from src.core.domain.entities.download_request import RequestStatus, ContentType, FailStatus, DownloadRequest
from src.core.domain.exceptions.downloader import *
from src.core.domain.exceptions.file_storage import *


class DownloaderWorker:

    def __init__(self, request_repo: IDownloadRequestRepository, content_downloader: IContentDownloader,
                 file_storage: IFileStorage):
        self.request_repo = request_repo
        self.content_downloader = content_downloader
        self.file_storage = file_storage
        self.processing_requests = []

    def start(self):
        threading.Thread(target=self.download_loop).start()

    def download_loop(self):
        with concurrent.futures.ThreadPoolExecutor(5) as executor:
            while True:
                for req in self.request_repo.get_unfinished_requests():
                    if req.id in self.processing_requests:
                        continue

                    self.processing_requests.append(req.id)
                    executor.submit(self.download_routine, req)
                time.sleep(1)

    def download_routine(self, req: DownloadRequest):
        try:

            self.request_repo.update_status(req.id, RequestStatus.downloading_content)
            file_path = self.content_downloader.download(req.download_link, req.content_type)

            self.request_repo.update_status(req.id, RequestStatus.uploading)
            public_link = self.file_storage.upload(file_path)
            os.remove(file_path)

            self.request_repo.update_content_link(req.id, public_link)

        except ContentDownloaderException as ex:
            self.request_repo.update_fail_status(req.id, to_fail_status(ex))
        except FileStorageException:
            self.request_repo.update_fail_status(req.id, FailStatus.file_storage_ex)
        except requests.exceptions.RequestException as e:
            self.request_repo.update_fail_status(req.id, FailStatus.requests_ex)
        except Exception as e:
            logging.exception(e)
            self.request_repo.update_fail_status(req.id, FailStatus.unexpected_ex)

        self.request_repo.update_status(req.id, RequestStatus.finished)
        self.processing_requests.remove(req.id)
