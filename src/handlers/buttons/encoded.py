import re

from aiogram import Router, F
from aiogram.types import Message

from database import User
from formater import send_solution

encoded_router = Router()


@encoded_router.message(F.text.regexp(
    re.compile(r'^SLVR:\?id=(\d{3,12}):([a-z-0-9]+)\.sdamgia\.ru:([a-f0-9,]+)$')).as_('match'))
async def on_encoded_message(message: Message, match: re.Match[str], user: User):
    test_id = match.group(1)
    hostname = match.group(2)

    try:
        encoded = [str(int(x, 16)) for x in (match.group(3).split(','))]
    except Exception:
        return await message.reply('❌ Неверная сигнатура')

    await send_solution(message.bot, message.from_user, user, hostname, test_id, encoded)
