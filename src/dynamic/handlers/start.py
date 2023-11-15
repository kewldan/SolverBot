from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import assets
import config
from bot import SolveBot


def get_keyboard(user_id: int):
    builder = ReplyKeyboardBuilder()

    builder.button(text='🧠 Решить')
    builder.button(text='📊 Статистика')
    if user_id in config.config['bot']['owners']:
        builder.button(text='💻 Администрирование')

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


@SolveBot.router.message(CommandStart())
async def on_start_command(message: Message):
    await message.answer_photo(assets.header, '👋 Привет, это бот для решения вариантов с сайта Сдам ГИА, '
                                              'полностью бесплатный и без рекламы. Бот создавался на некоммерческой '
                                              'основе. Всем спасибо за использование и активность!\n'
                                              '\n'
                                              f'Обратная связь: /support',
                               reply_markup=get_keyboard(message.from_user.id))
