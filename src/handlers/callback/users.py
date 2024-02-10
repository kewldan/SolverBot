import html

from aiogram import F, Router
from aiogram.types import CallbackQuery

import api
from db.database import users
from db.types.user import User

users_router = Router()


@users_router.callback_query(F.data == 'users', F.from_user.id.in_(api.config.bot.owners))
async def on_distribute_callback(query: CallbackQuery):
    users_response = []

    async for user in users.find():
        user = User(**user)
        if user.username:
            identity = html.escape(f'@{user.username}')
        else:
            identity = f'<code>{user.id}</code>'
        users_response.append(
            f'{len(users_response) + 1}. {identity} - {user.solved}')

    response = '\n'.join(users_response)
    await query.message.edit_text(f'<b>Пользователи ({len(users_response)}):</b>\n\n{response}')
