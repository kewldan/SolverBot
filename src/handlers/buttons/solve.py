from re import Match

from aiogram import F, Router
from aiogram.types import Message

from db.database import User
from formater import send_solution

solve_router = Router()


@solve_router.message(F.text, F.text == '🚀 Решить')
async def on_solve_button(message: Message):
    await message.answer(
        '<b>🤔 Чтобы решить вариант, отправьте ссылку боту сообщением</b>\n'
        '\n'
        'Например: https://oge.sdamgia.ru/test?id=54697659\n'
        '\n'
        'Теперь вы можете просто отправить номер варианта, например <code>54697659</code>, '
        'и потом выбрать платформу!')


@solve_router.message(F.text, F.text.regexp(r'^(https://[a-z\-]+\.sdamgia\.ru)/test\?id=(\d+)$').as_('m'))
async def on_solve_url_message(message: Message, m: Match[str], user: User):
    hostname = m.group(1)
    test_id = m.group(2)

    await send_solution(message.bot, message.from_user, user, hostname, test_id)
