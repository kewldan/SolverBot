import html
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config
from database import User

users_router = Router()


@users_router.callback_query(F.data.regexp(re.compile(r'^users(_(\d+))?$')).as_('match'),
                             F.from_user.id.in_(config.bot.owners))
async def on_distribute_callback(query: CallbackQuery, match: re.Match[str]):
    page = int(match.group(2) or '0')

    page_count = await User.count() // 50 + 1

    builder = InlineKeyboardBuilder()

    sizes = []
    if page > 0:
        builder.button(text=f'⬅️ Назад к {page}', callback_data=f'users_{page - 1}')
        sizes += [1]

    if page + 1 < page_count:
        builder.button(text=f'Вперёд к {page + 2} ➡️', callback_data=f'users_{page + 1}')
        if len(sizes):
            sizes[0] += 1
        else:
            sizes += [1]

    if page > 0:
        builder.button(text='⏮️ К началу', callback_data='users_0')
        sizes += [1]

    if page + 1 < page_count:
        builder.button(text='К концу ⏭️', callback_data=f'users_{page_count - 1}')
        if len(sizes) == 2:
            sizes[1] += 1
        else:
            sizes += [1]

    builder.adjust(*sizes)

    users_response = f'<b>Страница {page + 1}</b>\n\n'

    i = 1 + page * 50
    async for user in User.find(skip=page * 50, limit=50):
        if user.username:
            identity = html.escape(f'@{user.username}')
        else:
            identity = f'<code>{user.user_id}</code>'
        users_response += f'{i}. {identity}\n'
        i += 1
    await query.message.edit_text(users_response, reply_markup=builder.as_markup())
