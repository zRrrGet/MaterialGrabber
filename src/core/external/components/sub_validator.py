from typing import Union

from aiogram import Bot
from src.core.domain.components.sub_validator import ISubValidator
from aiogram.exceptions import TelegramBadRequest


class SubValidator(ISubValidator):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def validate(self, chat_id: Union[int, str], user_id: int) -> bool:
        try:
            await self.bot.get_chat_member(chat_id, user_id)
            return True
        except TelegramBadRequest:
            return False
