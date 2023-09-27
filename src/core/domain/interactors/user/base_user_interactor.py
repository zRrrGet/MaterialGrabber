from src.core.domain.repositories.user_repo import IUserRepository
from src.core.domain.repositories.channel_repo import IChannelRepository
from src.core.domain.components.sub_validator import ISubValidator

from src.core.domain.entities.channel import Channel
from src.core.domain.entities.user import User

from .user_interactor import IUserInteractor


class UserInteractor(IUserInteractor):

    def __init__(self, user_repo: IUserRepository, channel_repo: IChannelRepository, sub_validator: ISubValidator):
        self.user_repo = user_repo
        self.channel_repo = channel_repo
        self.sub_validator = sub_validator

    def ensure_user(self, tg_id: int) -> int:
        user = self.user_repo.get_user_by_tg(tg_id)
        if not user:
            return self.user_repo.add_user(User(None, tg_id, False))

        return user.id

    async def get_unsubscribed_channels(self, user_id: int) -> list[Channel]:
        user = self.user_repo.get_user(user_id)
        if user.subscribed_on_channels:
            return []

        left_channels = []
        for channel in self.channel_repo.get_channels():
            if not await self.sub_validator.validate(channel.chat_id, user.tg_id):
                left_channels.append(channel)

        self.user_repo.change_sub(user_id, not left_channels)
        return left_channels
