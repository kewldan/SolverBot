import asyncio
import html
from datetime import datetime
from typing import Optional

import pymongo
from aiogram import types, Bot
from aiogram.exceptions import AiogramError
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from beanie import Document
from kwldn_bot.database import BaseUser

from config import config, AccountData


async def notify(bot: Bot, owner: int, identity: str, markup: InlineKeyboardMarkup):
    try:
        await bot.send_message(owner, f'🔔 Зарегистрирован новый пользователь - {identity}',
                               reply_markup=markup)
    except AiogramError:
        pass


class User(BaseUser):
    blocked: bool = False
    referral: Optional[str] = None
    account: AccountData | None = None


class Test(Document):
    timestamp: datetime
    hostname: str
    user_id: int | None = None
    test_id: str
    problems: list[str]

    class Settings:
        indexes = [
            pymongo.IndexModel([
                ('hostname', pymongo.ASCENDING),
                ('test_id', pymongo.ASCENDING)
            ])
        ]


class Problem(Document):
    hostname: str
    internal_id: str | None
    problem_id: str
    solution: str | None
    answer: str | None

    class Settings:
        indexes = [
            pymongo.IndexModel(
                [
                    ("hostname", pymongo.ASCENDING),
                    ("internal_id", pymongo.ASCENDING),
                ]
            ),
            pymongo.IndexModel(
                [
                    ("hostname", pymongo.ASCENDING),
                    ("problem_id", pymongo.ASCENDING)
                ]
            )
        ]


async def get_user(bot: Bot, event_user: types.User) -> User:
    user = await User.find_one(User.user_id == str(event_user.id))
    if not user:
        user = User(user_id=str(event_user.id), username=event_user.username, joined=datetime.now())
        await user.insert()
        builder = InlineKeyboardBuilder()
        if event_user.url:
            builder.button(text='Открыть', url=event_user.url)
        if event_user.username:
            identity = html.escape(f'@{event_user.username}')
        else:
            identity = f'[<code>{event_user.id}</code>]'
        tasks = []
        for owner in config.bot.owners:
            tasks.append(notify(bot, owner, identity, builder.as_markup()))
        await asyncio.gather(*tasks)
    if user.username != event_user.username:
        user.username = event_user.username
        await user.save()
    return user
