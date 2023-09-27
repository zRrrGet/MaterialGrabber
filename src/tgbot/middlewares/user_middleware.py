from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update

from src.core.external.controllers.user_controller import UserController


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user_controller: UserController = data['user_controller']
        data['user_id'] = user_controller.ensure_user(data)
        return await handler(event, data)
