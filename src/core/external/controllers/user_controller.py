from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from src.core.domain.interactors.user.user_interactor import IUserInteractor


class UserController:

    def __init__(self, user_interactor: IUserInteractor):
        self.user_interactor = user_interactor

    def ensure_user(self, message: Message):
        self.user_interactor.ensure_user(message.from_user.id)

    async def is_subscribed(self, callback: Union[Message, CallbackQuery]) -> bool:
        return not await self.user_interactor.get_unsubscribed_channels(callback.from_user.id)

    async def get_unsubscribed_channels(self, manager: DialogManager) -> list[list]:
        left_channels = await self.user_interactor.get_unsubscribed_channels(manager.event.from_user.id)
        return list(map(lambda c: [c.join_link], left_channels))
