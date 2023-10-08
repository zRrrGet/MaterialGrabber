from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class IstockvideoClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/istockvideos-downloader.php'
