import html
import math
import time

import motor.motor_asyncio
from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

import api

client = motor.motor_asyncio.AsyncIOMotorClient(api.config.bot.mongo)
database = client[api.config.bot.database]
users = database['users']


async def get_user(bot: Bot, event_user: types.User):
    user = await users.find_one({'id': event_user.id})
    if not user:
        await users.insert_one({
            'id': event_user.id,
            'username': event_user.username,
            'solved': 0,
            'joined': math.floor(time.time())
        })
        builder = InlineKeyboardBuilder()
        if event_user.url:
            builder.button(text='Открыть', url=event_user.url)
        if event_user.username:
            identity = html.escape(f'@{event_user.username}')
        else:
            identity = f'[<code>{event_user.id}</code>]'
        for owner in api.config.bot.owners:
            try:
                await bot.send_message(owner, f'🔔 Зарегистрирован новый пользователь - {identity}',
                                       reply_markup=builder.as_markup())
            except TelegramBadRequest:
                pass
        user = await users.find_one({'id': event_user.id})
    return user


async def capture_referral(user_id: int, referral: str):
    await users.update_one({'id': user_id}, {
        '$set': {
            'referral': referral
        }
    })
