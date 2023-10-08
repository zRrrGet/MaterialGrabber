from typing import Union

from aiogram import Bot
from aiogram.types import ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator

from src.core.domain.components.sub_validator import ISubValidator
from aiogram.exceptions import TelegramBadRequest


class SubValidator(ISubValidator):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def validate(self, chat_id: Union[int, str], user_id: int) -> bool:
        try:
            user_status = await self.bot.get_chat_member(chat_id, user_id)
            return (isinstance(user_status, ChatMemberMember) or
                    isinstance(user_status, ChatMemberAdministrator) or
                    isinstance(user_status, ChatMemberOwner))
        except TelegramBadRequest:
            return False
