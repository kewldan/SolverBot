import html

from aiogram import F
from aiogram.types import CallbackQuery

from bot import SolveBot
from config import config
from db.database import users
from db.types.user import User
from utils import get_timestamp


@SolveBot.router.callback_query(F.data == 'users', F.from_user.id.in_(config['bot']['owners']))
async def on_distribute_callback(query: CallbackQuery):
    users_response = []

    async for user in users.find():
        user = User(**user)
        users_response.append(
            f'<b>{len(users_response) + 1}.</b> {html.escape(("@" + user.username) if user.username else "")} [<code>{user.id}</code>] - '
            f'<code>{user.solved}</code> | {get_timestamp(user.joined)}'
            f'{html.escape((" через " + user.referral) if user.referral else "")}')

    response = "\n".join(users_response)
    await query.message.edit_text(f'<b>Пользователи ({len(users_response)}):</b>\n\n{response}')
