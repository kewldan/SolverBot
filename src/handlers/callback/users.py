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
        users_response.append(
            f'<b>{len(users_response) + 1}.</b> {html.escape(("@" + user.username) if user.username else "")} [<code>{user.id}</code>] - '
            f'<code>{user.solved}</code>')

    response = "\n".join(users_response)
    await query.message.edit_text(f'<b>Пользователи ({len(users_response)}):</b>\n\n{response}')
