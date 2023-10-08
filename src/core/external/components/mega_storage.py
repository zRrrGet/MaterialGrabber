import os
import re
from src.core.domain.components.file_storage import IFileStorage
from src.core.domain.exceptions.file_storage import *


class MegaStorage(IFileStorage):

    def __init__(self, mega_folder: str, cloud_folder: str):
        self.mega_folder = mega_folder
        self.cloud_folder = cloud_folder

    def upload(self, file_path: str) -> str:
        os.popen(f'{self.mega_folder}\\mega-put -c {file_path} {self.cloud_folder}').read()
        export_response = os.popen(f'{self.mega_folder}\\mega-export -a  --expire=1d {self.cloud_folder}/'
                                   f'{os.path.basename(file_path)}').read()

        match = re.search("(?P<url>https?://[^\s]+)", export_response)
        if not match:
            raise UploadException()

        return match.group('url')
