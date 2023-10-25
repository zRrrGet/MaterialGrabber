from typing import Optional

from src.core.domain.repositories.user_repo import IUserRepository
from src.core.domain.repositories.channel_repo import IChannelRepository
from src.core.domain.components.sub_validator import ISubValidator

from src.core.domain.entities.channel import Channel
from src.core.domain.entities.user import User

from .user_interactor import IUserInteractor


class UserInteractor(IUserInteractor):

    def __init__(self, user_repo: IUserRepository,
                 channel_repo: IChannelRepository, sub_validator: ISubValidator):
        self.user_repo = user_repo
        self.channel_repo = channel_repo
        self.sub_validator = sub_validator

    def ensure_user(self, tg_id: int, username: Optional[str], full_name: str) -> int:
        user = self.user_repo.get_user_by_tg(tg_id)
        if not user:
            return self.user_repo.add_user(User(None, tg_id, username, full_name, None, False, False, False))

        return user.id

    async def get_unsubscribed_channels(self, user_id: int) -> list[Channel]:
        user = self.user_repo.get_user(user_id)
        # if user.subscribed_on_channels:
        #     return []

        left_channels = []
        for channel in self.channel_repo.get_channels():
            if not await self.sub_validator.validate(channel.chat_id, user.tg_id):
                left_channels.append(channel)

        self.user_repo.update_sub(user_id, not left_channels)
        return left_channels

    def are_rules_accepted(self, user_id: int) -> bool:
        return self.user_repo.get_user(user_id).accepted_rules

    def update_rules_agreement(self, user_id: int, agreed_with_rules: bool):
        self.user_repo.update_rules_agreement(user_id, agreed_with_rules)

    def reset_sub_all(self):
        self.user_repo.reset_sub_all()
