from src.core.domain.interactors.user.user_interactor import IUserInteractor


class UserController:

    def __init__(self, user_interactor: IUserInteractor):
        self.user_interactor = user_interactor

    def ensure_user(self, data: dict) -> int:
        return self.user_interactor.ensure_user(data['event_from_user'].id)

    async def is_subscribed(self, user_id: int) -> bool:
        return not await self.user_interactor.get_unsubscribed_channels(user_id)

    async def get_unsubscribed_channels(self, user_id: int) -> list[list]:
        left_channels = await self.user_interactor.get_unsubscribed_channels(user_id)
        return list(map(lambda c: [c.join_link], left_channels))
