from typing import Union

from aiogram import F, types, Router
from kwldn_bot.utils import get_timestamp

from db.types.user import User

statistics_router = Router()


@statistics_router.callback_query(F.data == 'statistics')
@statistics_router.message(F.text == '📊 Статистика')
async def on_statistics_callback(message: Union[types.Message, types.CallbackQuery], user: User):
    if type(message) is types.Message:
        func = message.answer
    else:
        func = message.message.edit_text

    joined = get_timestamp(user.joined)

    await func(
        text=f'Статистика @{user.username if user.username else "none"}\n'
             f'\n'
             f'🆔 ID: <code>{user.id}</code>\n\n'
             f'📅 Дата регистрации: <code>{joined}</code>\n'
             f'✅ Решено вариантов: <code>{user.solved}</code>\n'
             '\n'
             f'Обратная связь: /support')
