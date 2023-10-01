from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import assets
from bot import SolveBot


def get_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🧠 Решить')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


@SolveBot.router.message(CommandStart())
async def on_start_command(message: Message):
    await message.answer_photo(assets.header, 'Спасибо, что пользуетесь нашим ботом!\n'
                                              f'Ваш ID в системе - <code>{message.from_user.id}</code>\n\n'
                                              f'Обратная связь @kewldan',
                               reply_markup=get_keyboard())
