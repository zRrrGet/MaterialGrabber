from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class AgefotostockClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/agefotostock-downloader.php'
