from src.core.external.components.content_downloader.sources.base.fetchpik import FetchpikClient


class MotionarrayClient(FetchpikClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/motionarray-downloader.php'
