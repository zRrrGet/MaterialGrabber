from typing import Optional

from sqlalchemy import update, select

from .alchemy_base import AlchemyBaseRepo
from src.core.external.orm.models import User
from src.core.domain.entities.user import User as EntityUser
from src.core.domain.repositories.user_repo import IUserRepository

from src.core.external.orm.mappers.user_mapper import UserMapper


class AlchemyUserRepo(IUserRepository, AlchemyBaseRepo):

    def add_user(self, user: EntityUser) -> int:
        session = self.session()
        new_user = UserMapper.to_model(user)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()

        return new_user.id

    def get_user(self, user_id: int) -> Optional[EntityUser]:
        session = self.session()
        user = session.get(User, user_id)
        session.close()
        if not user:
            return None

        return UserMapper.to_entity(user)

    def get_user_by_tg(self, tg_id: int) -> Optional[EntityUser]:
        session = self.session()
        user = session.scalars(select(User).filter_by(tg_id=tg_id)).one_or_none()
        if not user:
            return None

        return UserMapper.to_entity(user)

    def update_sub(self, user_id: int, subscribed: bool):
        self.execute(update(User).where(User.id == user_id).values({'subscribed_on_channels': subscribed}))

    def update_rules_agreement(self, user_id: int, agreed_with_rules: bool):
        self.execute(update(User).where(User.id == user_id).values({'accepted_rules': agreed_with_rules}))

    def reset_sub_all(self):
        self.execute(update(User).values({'subscribed_on_channels': False}))
