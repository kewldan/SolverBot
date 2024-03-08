from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import api
import assets
from db.database import User

start_router = Router()


def get_keyboard(user_id: int):
    builder = ReplyKeyboardBuilder()

    builder.button(text='🚀 Решить')
    builder.button(text='📊 Статистика')
    if user_id in api.config.bot.owners:
        builder.button(text='💻 Администрирование')

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


@start_router.message(CommandStart())
async def on_start_command(message: Message, user: User):
    if not user.referral:
        arguments = message.text.split()[1:]
        if len(arguments) > 0:
            user.referral = arguments[0]
            await user.save()

    content = (
        '⛔️ Бот работает только для ОГЭ и некоторых предметов ЕГЭ, ВПР временно не доступен. Все платформы будут поддерживатся до конца недели\n\n'
        '👋 Привет, это бот для решения вариантов с сайта Сдам ГИА,'
        'полностью бесплатный и без рекламы. Бот разрабатывается на некоммерческой '
        'основе.\n'
        '\n'
        f'Обратная связь: /support')

    await message.answer_photo(assets.header, content,
                               reply_markup=get_keyboard(message.from_user.id))
