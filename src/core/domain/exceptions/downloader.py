from src.core.domain.exceptions import MaterialGrabberException
from src.core.domain.entities.download_request import FailStatus


class ContentDownloaderException(MaterialGrabberException):
    pass


class NoResultsFoundException(ContentDownloaderException):
    pass


class EmptyFileException(ContentDownloaderException):
    pass


class EndpointParseException(ContentDownloaderException):
    pass


class LinkPrepareException(ContentDownloaderException):
    pass


class UnsupportedDomainException(ContentDownloaderException):
    pass


def to_fail_status(ex) -> FailStatus:
    return {
        NoResultsFoundException: FailStatus.no_results_found,
        EmptyFileException: FailStatus.empty_file,
        EndpointParseException: FailStatus.endpoint_parse_ex,
        LinkPrepareException: FailStatus.link_prepare_ex,
        UnsupportedDomainException: FailStatus.unsupported_domain
    }[ex.__class__]
