import typing

from aiogram.filters import Filter
from aiogram.types import Message
from tgbot.config import Config


class AdminFilter(Filter):

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def __call__(self, message: Message, config: Config) -> bool:
        if self.is_admin is None:
            return False

        return (message.from_user.id in config.tg_bot.admin_ids) == self.is_admin
