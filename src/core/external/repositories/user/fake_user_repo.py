from typing import Optional

from src.core.domain.entities.user import User
from src.core.domain.repositories.user_repo import IUserRepository


class FakeUserRepo(IUserRepository):

    def __init__(self):
        self.created_user = False
        self.sub = False

    def add_user(self, user: User):
        self.sub = user.subscribed_on_channels
        self.created_user = True

    def get_user(self, user_id: int) -> Optional[User]:
        if self.created_user:
            return User(user_id, 123, self.sub)

        return None

    def get_user_by_tg(self, tg_id: int) -> Optional[User]:
        if self.created_user:
            return User(1, tg_id, self.sub)

        return None

    def change_sub_by_tg(self, tg_id: int, subscribed: bool) -> Optional[User]:
        self.sub = subscribed
