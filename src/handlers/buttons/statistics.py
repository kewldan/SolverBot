from typing import Union

from aiogram import F, types, Router

from db.database import User

statistics_router = Router()


@statistics_router.callback_query(F.data == 'statistics')
@statistics_router.message(F.text == '📊 Статистика')
async def on_statistics_callback(message: Union[types.Message, types.CallbackQuery], user: User):
    if type(message) is types.Message:
        # noinspection PyTypeChecker
        func = message.answer
    else:
        # noinspection PyTypeChecker
        func = message.message.edit_text

    joined = user.joined.strftime('%H:%M:%S %d.%m.%Y')

    await func(
        text=f'Статистика @{user.username if user.username else "none"}\n'
             f'\n'
             f'🆔 ID: <code>{user.id}</code>\n\n'
             f'📅 Дата регистрации: <code>{joined}</code>\n'
             f'✅ Решено вариантов: <code>{user.solved}</code>\n'
             '\n'
             f'Обратная связь: /support')
