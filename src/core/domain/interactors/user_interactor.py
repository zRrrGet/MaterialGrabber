from src.core.domain.entities.user import User
from src.core.domain.repositories.user_repo import IUserRepository


class UserInteractor:

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def ensure_user(self, tg_id: int):
        if not self.user_repo.get_user_by_tg(tg_id):
            self.user_repo.add_user(User(None, tg_id, False))

    def is_user_subscribed(self, tg_id: int) -> bool:
        user = self.user_repo.get_user_by_tg(tg_id)
        return user.subscribed_on_channels
