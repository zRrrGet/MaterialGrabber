from aiogram_dialog import DialogManager
from src.core.domain.interactors.user.user_interactor import IUserInteractor


class UserController:

    def __init__(self, user_interactor: IUserInteractor):
        self.user_interactor = user_interactor

    def ensure_user(self, data: dict) -> int:
        user = data['event_from_user']
        return self.user_interactor.ensure_user(user.id, user.username, user.full_name)

    async def is_subscribed(self, manager: DialogManager) -> bool:
        user_id = manager.middleware_data['user_id']
        return not await self.user_interactor.get_unsubscribed_channels(user_id)

    async def get_unsubscribed_channels(self, manager: DialogManager) -> list[list]:
        user_id = manager.middleware_data['user_id']
        left_channels = await self.user_interactor.get_unsubscribed_channels(user_id)
        return list(map(lambda c: [c.join_link], left_channels))

    def accept_rules(self, manager: DialogManager):
        user_id = manager.middleware_data['user_id']
        self.user_interactor.update_rules_agreement(user_id, True)

    def are_rules_accepted(self, manager: DialogManager):
        user_id = manager.middleware_data['user_id']
        return self.user_interactor.are_rules_accepted(user_id)
