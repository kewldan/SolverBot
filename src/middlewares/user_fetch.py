from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from db.database import get_user


class UserFetchMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        data['user'] = await get_user(event.bot, event.from_user)

        return await handler(event, data)
