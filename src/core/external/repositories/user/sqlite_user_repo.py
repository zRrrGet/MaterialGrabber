from typing import Optional

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import update, select

from src.core.external.orm.models import User
from src.core.domain.entities.user import User as EntityUser
from src.core.domain.repositories.user_repo import IUserRepository


class SqliteUserRepo(IUserRepository):

    def __init__(self, session: scoped_session):
        self.session = session

    def add_user(self, user: EntityUser) -> int:
        session = self.session()
        new_user = User(id=user.id, tg_id=user.tg_id, subscribed_on_channels=user.subscribed_on_channels)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()

        return new_user.id

    def get_user(self, user_id: int) -> Optional[EntityUser]:
        session = self.session()
        user = session.get(User, user_id)
        session.close()
        return EntityUser(id=user.id, tg_id=user.tg_id, subscribed_on_channels=user.subscribed_on_channels)

    def get_user_by_tg(self, tg_id: int) -> Optional[EntityUser]:
        session = self.session()
        user = session.scalars(select(User).filter_by(tg_id=tg_id)).one_or_none()
        if not user:
            return None

        return EntityUser(id=user.id, tg_id=user.tg_id, subscribed_on_channels=user.subscribed_on_channels)

    def change_sub(self, user_id: int, subscribed: bool):
        session = self.session()
        session.execute(
            update(User)
            .where(User.id == user_id)
            .values({'subscribed_on_channels': subscribed})
            .execution_options(synchronize_session='fetch')
        )
        session.commit()
        session.close()
