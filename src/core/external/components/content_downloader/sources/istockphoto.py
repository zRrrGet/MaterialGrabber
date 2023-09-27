from .depositphotos import DepositphotosClient


class IstockphotoClient(DepositphotosClient):

    @property
    def endpoint(self) -> str:
        return 'https://toolxox.com/dl/1/is_1.0/tmp/6GbwYclEL.php'

    @staticmethod
    def prepare_request_link(link: str) -> str:
        return link
