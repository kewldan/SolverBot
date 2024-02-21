import asyncio
import html
from datetime import datetime
from typing import Optional

from aiogram import types, Bot
from aiogram.exceptions import AiogramError
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient

import api

client = AsyncIOMotorClient(api.config.bot.mongo)


async def notify(bot: Bot, owner: int, identity: str, markup: InlineKeyboardMarkup):
    try:
        await bot.send_message(owner, f'🔔 Зарегистрирован новый пользователь - {identity}',
                               reply_markup=markup)
    except AiogramError:
        pass


class User(Document):
    user_id: int
    username: Optional[str] = None
    solved: int = 0
    joined: datetime
    referral: Optional[str] = None


async def get_user(bot: Bot, event_user: types.User) -> User:
    user = await User.find_one(User.user_id == event_user.id)
    if not user:
        user = User(user_id=event_user.id, username=event_user.username, joined=datetime.now())
        await user.insert()
        builder = InlineKeyboardBuilder()
        if event_user.url:
            builder.button(text='Открыть', url=event_user.url)
        if event_user.username:
            identity = html.escape(f'@{event_user.username}')
        else:
            identity = f'[<code>{event_user.id}</code>]'
        tasks = []
        for owner in api.config.bot.owners:
            tasks.append(notify(bot, owner, identity, builder.as_markup()))
        await asyncio.gather(*tasks, return_exceptions=False)
    if user.username != event_user.username:
        user.username = event_user.username
        await user.save()
    return user


async def connect():
    await init_beanie(database=client[api.config.bot.database],
                      document_models=[User])
