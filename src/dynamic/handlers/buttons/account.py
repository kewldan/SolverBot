from datetime import datetime
from typing import Union

from aiogram import F, types

from bot import SolveBot
from db.types.user import User


@SolveBot.router.callback_query(F.data == 'account')
@SolveBot.router.message(F.text == '⚙️ Аккаунт')
async def on_account_view_callback(message: Union[types.Message, types.CallbackQuery], user: User):
    if type(message) is types.Message:
        func = message.answer
    else:
        func = message.message.edit_text

    joined = datetime.fromtimestamp(user.joined).strftime("%d.%m.%Y %H:%M")

    await func(
        text=f'Аккаунт @{user.username}\n'
             f'\n'
             f'🆔 ID: <code>{user.id}</code>\n\n'
             f'📅 Дата регистрации: <code>{joined}</code>\n'
             f'✅ Решено вариантов: <code>{user.solved}</code>\n'
             f'💵 Баланс: <code>0₽</code>')
