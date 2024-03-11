from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from database import User, Test

statistics_router = Router()


@statistics_router.callback_query(F.data == 'statistics')
@statistics_router.message(F.text == '📊 Статистика')
async def on_statistics_callback(message: Message | CallbackQuery, user: User):
    if type(message) is types.Message:
        # noinspection PyTypeChecker
        func = message.answer
    else:
        # noinspection PyTypeChecker
        func = message.message.edit_text

    joined = user.joined.strftime('%H:%M:%S %d.%m.%Y')
    referral_link = await create_start_link(message.bot, f'u{message.from_user.id}')

    referrals = await User.find(User.referral == f'u{message.from_user.id}').count()
    solved = await Test.find(Test.user_id == message.from_user.id).count()

    await func(
        text=f'Статистика @{user.username if user.username else "none"}\n'
             f'\n'
             f'🆔 ID: <code>{user.user_id}</code>\n\n'
             f'📅 Дата регистрации: <code>{joined}</code>\n'
             f'✅ Решено вариантов: <code>{solved}</code>\n' +
             (f'🔒 Реферал: <code>{user.referral}</code>\n' if user.referral else '') +
             '\n'
             f'👥 Ваши рефералы: {referrals}\n'
             f'🔗 Ваша реферальная <a href="{referral_link}">ссылка</a>\n'
             '\n'
             f'Обратная связь: /support')
