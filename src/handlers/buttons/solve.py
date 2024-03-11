import re

from aiogram import F, Router
from aiogram.types import Message

from database import User
from formater import send_solution

solve_router = Router()


@solve_router.message(F.text == '🚀 Решить')
async def on_solve_button(message: Message):
    await message.answer(
        '<b>🤔 Чтобы решить вариант, отправьте ссылку боту сообщением</b>\n'
        '\n'
        'Например: https://math-oge.sdamgia.ru/test?id=54697659\n'
        '\n'
        'Теперь вы можете просто отправить номер варианта, например <code>54697659</code>, '
        'и потом выбрать платформу!')


@solve_router.message(F.text.regexp(re.compile(r'^https://([a-z0-9\-]+)\.sdamgia\.ru/test\?id=(\d+)$')).as_('match'))
async def on_solve_url_message(message: Message, match: re.Match[str], user: User):
    await send_solution(message.bot, message.from_user, user, match.group(1), match.group(2))
