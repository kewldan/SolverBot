import html
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import api
from db import database
from db.types.user import User


class UserFetchMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        user = User(**await database.get_user(event.from_user.id, event.from_user.username))

        if user.username != event.from_user.username:
            await database.users.update_one({'id': event.from_user.id},
                                            {'$set': {'username': event.from_user.username}})

        data['user'] = user

        builder = InlineKeyboardBuilder()
        if event.from_user.url:
            builder.button(text='Открыть', url=event.from_user.url)
        if event.from_user.username:
            identity = html.escape(f'@{event.from_user.username}')
        else:
            identity = f'[<code>{event.from_user.id}</code>]'
        for owner in api.config.bot.owners:
            await event.bot.send_message(owner, f'🔔 Зарегистрирован новый пользователь - {identity}',
                                         reply_markup=builder.as_markup())

        return await handler(event, data)
