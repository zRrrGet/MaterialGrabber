from aiogram.types import Message
from src.core.domain.interactors.user_interactor import UserInteractor


class UserController:

    def __init__(self, user_interactor: UserInteractor):
        self.user_interactor = user_interactor

    def ensure_user(self, message: Message):
        self.user_interactor.ensure_user(message.from_user.id)

    def is_user_subscribed(self, message: Message) -> bool:
        return self.user_interactor.is_user_subscribed(message.from_user.id)
