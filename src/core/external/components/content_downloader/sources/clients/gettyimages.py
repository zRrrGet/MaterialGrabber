from .istockphoto import IstockphotoClient


class GettyimagesClient(IstockphotoClient):

    @property
    def endpoint_temp_root(self) -> str:
        return 'https://toolxox.com/dl/2/dlgrab_1/'
