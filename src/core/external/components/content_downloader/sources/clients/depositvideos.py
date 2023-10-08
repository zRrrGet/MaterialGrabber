from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class DepositvideosClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/depositphotos-videos-downloader.php'
