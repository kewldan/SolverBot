from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from db import database
from db.types.user import User


class UserFetchMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        user = User(**await database.get_user(event.bot, event.from_user))

        if user.username != event.from_user.username:
            await database.users.update_one({'id': event.from_user.id},
                                            {'$set': {'username': event.from_user.username}})

        data['user'] = user

        return await handler(event, data)
