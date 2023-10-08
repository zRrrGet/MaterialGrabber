from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from .session_factory import ISessionFactory


class BaseSessionFactory(ISessionFactory):

    def create(self) -> Session:
        session = Session()

        adapter = HTTPAdapter(max_retries=Retry(total=4, backoff_factor=1, allowed_methods=None,
                                                status_forcelist=[429, 500, 502, 503, 504]))
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update({'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'})
        session.hooks = {'response': lambda r, *args, **kwargs: r.raise_for_status()}

        session.trust_env = False
        session.verify = False

        return session
