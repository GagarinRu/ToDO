from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from typing import Any, Callable, Dict, Awaitable

from services.bot_context import bot_context


class AuthMiddleware(BaseMiddleware):
    """Middleware для аутентификации пользователей."""

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Обрабатывает входящие события."""
        if isinstance(event, Message):
            user = event.from_user
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            chat_id = event.message.chat.id if event.message else None
        else:
            return await handler(event, data)
        user_data = await bot_context.authenticate_user(user, chat_id)
        data["user"] = user_data

        return await handler(event, data)
