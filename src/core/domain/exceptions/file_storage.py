from src.core.domain.exceptions import MaterialGrabberException


class FileStorageException(MaterialGrabberException):
    pass


class UploadException(FileStorageException):
    pass
