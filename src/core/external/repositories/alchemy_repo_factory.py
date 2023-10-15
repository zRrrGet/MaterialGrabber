from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy_utils import database_exists

from src.core.domain.repositories.repo_factory import IRepositoryFactory
from src.core.domain.repositories.user_repo import IUserRepository
from src.core.domain.repositories.channel_repo import IChannelRepository
from src.core.domain.repositories.download_request_repo import IDownloadRequestRepository

from src.core.external.orm.models import Base
from src.core.external.repositories.alchemy_user_repo import AlchemyUserRepo
from src.core.external.repositories.alchemy_channel_repo import AlchemyChannelRepo
from src.core.external.repositories.alchemy_download_request_repo import AlchemyDownloadRequestRepo


class AlchemyRepoFactory(IRepositoryFactory):

    def __init__(self, db_url: str):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine, checkfirst=True)
        # Base.metadata.drop_all(engine)

        session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        self.session = scoped_session(session_factory)

    def create_user_repo(self) -> IUserRepository:
        return AlchemyUserRepo(self.session)

    def create_channel_repo(self) -> IChannelRepository:
        return AlchemyChannelRepo(self.session)

    def create_download_request_repo(self) -> IDownloadRequestRepository:
        return AlchemyDownloadRequestRepo(self.session)
