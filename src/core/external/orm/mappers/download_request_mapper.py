from src.core.external.orm.models import DownloadRequest
from src.core.domain.entities.download_request import DownloadRequest as EntityDownloadRequest


class DownloadRequestMapper:

    @staticmethod
    def to_entity(model: DownloadRequest) -> EntityDownloadRequest:
        return EntityDownloadRequest(id=model.id, user_id=model.user_id, download_link=model.download_link,
                                     content_link=model.content_link, content_type=model.content_type,
                                     status=model.status, fail_status=model.fail_status,
                                     created_date=model.created_date)

    @staticmethod
    def to_model(entity: EntityDownloadRequest) -> DownloadRequest:
        return DownloadRequest(id=entity.id, user_id=entity.user_id, download_link=entity.download_link,
                               content_link=entity.content_link, content_type=entity.content_type,
                               status=entity.status, fail_status=entity.fail_status,
                               created_date=entity.created_date)
