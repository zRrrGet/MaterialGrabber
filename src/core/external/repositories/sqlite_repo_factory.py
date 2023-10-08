from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy_utils import database_exists

from src.core.domain.repositories.repo_factory import IRepositoryFactory
from src.core.domain.repositories.user_repo import IUserRepository
from src.core.domain.repositories.channel_repo import IChannelRepository
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository

from src.core.external.orm.models import Base
from src.core.external.repositories.sqlite_user_repo import SqliteUserRepo
from src.core.external.repositories.sqlite_channel_repo import SqliteChannelRepo
from src.core.external.repositories.sqlite_download_request_repo import SqliteDownloadRequestRepo


class SqliteRepoFactory(IRepositoryFactory):

    def __init__(self, db_path: str):
        engine = create_engine(f'sqlite:///{db_path}')

        if not database_exists(engine.url):
            # Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

        session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        self.session = scoped_session(session_factory)

    def create_user_repo(self) -> IUserRepository:
        return SqliteUserRepo(self.session)

    def create_channel_repo(self) -> IChannelRepository:
        return SqliteChannelRepo(self.session)

    def create_download_request_repo(self) -> IDownloadRequestRepository:
        return SqliteDownloadRequestRepo(self.session)
