from .depositphotos_video import DepositphotosVideoClient


class IstockphotoVideoClient(DepositphotosVideoClient):

    @property
    def endpoint(self) -> str:
        return 'https://fetchpik.com/istockvideos-downloader.php'
