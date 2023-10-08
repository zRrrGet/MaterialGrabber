from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class GettyvideosClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/gettyvideos-downloader.php'
