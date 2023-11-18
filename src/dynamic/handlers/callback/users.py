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
            f'{len(users_response) + 1}. @{user.username} [<code>{user.id}</code>] - решено '
            f'<code>{user.solved}</code> {get_timestamp(user.joined)} <- {user.referral}')

    response = "\n".join(users_response)
    await query.message.edit_text(f'<b>Пользователи ({len(users_response)}):</b>\n\n{response}')
