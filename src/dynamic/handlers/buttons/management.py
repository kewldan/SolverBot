from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from bot import SolveBot


@SolveBot.router.message(F.text, F.text == '💻 Администрирование', F.from_user.id == config.config['bot']['owner'])
async def on_management_button(message: Message):
    builder = InlineKeyboardBuilder()

    builder.button(text='📢 Рассылка', callback_data='distribute')

    if type(message) is Message:
        func = message.answer
    else:
        func = message.message.edit_text

    await func(
        text='<b>Администрирование SolverBot</b>' + (
            '\n\n⚠️ <b>ВКЛЮЧЕН ТЕСТОВЫЙ РЕЖИМ</b> ⚠️' if config.config['bot'][
                'debug'] else ''),
        reply_markup=builder.as_markup())
