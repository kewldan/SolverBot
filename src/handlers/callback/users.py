import html

from aiogram import F, Router
from aiogram.types import CallbackQuery

import api
from db.database import User

users_router = Router()


@users_router.callback_query(F.data == 'users', F.from_user.id.in_(api.config.bot.owners))
async def on_distribute_callback(query: CallbackQuery):
    users_response = ''
    first = True
    count = await User.count()
    i = 1

    async for user in User.find():
        if user.username:
            identity = html.escape(f'@{user.username}')
        else:
            identity = f'<code>{user.user_id}</code>'
        users_response += f'{i}. {identity} - {user.solved}\n'
        i += 1
        if len(users_response) > 3900:
            if first:
                await query.message.edit_text(f'<b>Пользователи ({count}):</b>\n\n{users_response}')
                first = False
            else:
                await query.message.answer(users_response)
            users_response = ''
    if len(users_response) > 0:
        await query.message.answer(users_response)
