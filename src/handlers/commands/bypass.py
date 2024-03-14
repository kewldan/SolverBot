from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from assets import bypass, code

bypass_router = Router()


@bypass_router.message(Command('bypass'))
async def on_bypass_command(message: Message):
    await message.answer_video(bypass,
                               caption='<b>Вставьте этот код в консоль разработчика, когда у вас открыт вариант</b>\n'
                                       '\n'
                                       f'<pre>{code}</pre>\n'
                                       f'\n'
                                       f'<b>Отправьте боту строку, начиная с SLVR...</b>')
