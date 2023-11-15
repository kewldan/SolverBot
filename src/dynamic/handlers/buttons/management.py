from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from bot import SolveBot


@SolveBot.router.message(F.text, F.text == '💻 Администрирование', F.from_user.id.in_(config.config['bot']['owners']))
async def on_management_button(message: Message):
    builder = InlineKeyboardBuilder()

    builder.button(text='📢 Рассылка', callback_data='distribute')
    builder.button(text='🧑‍🎓 Пользователи', callback_data='users')

    builder.adjust(1, repeat=True)

    if type(message) is Message:
        func = message.answer
    else:
        func = message.message.edit_text

    me = await SolveBot.instance.get_me()

    await func(
        text=f'<b>Администрирование @{me.username}</b>' + (
            '\n\n⚠️ <b>ВКЛЮЧЕН ТЕСТОВЫЙ РЕЖИМ</b> ⚠️' if config.config['bot'][
                'debug'] else ''),
        reply_markup=builder.as_markup())
