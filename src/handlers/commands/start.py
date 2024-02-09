from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import api
import assets
from db.database import capture_referral
from db.types.user import User

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
            await capture_referral(user.id, arguments[0])

    content = ('👋 Привет, это бот для решения вариантов с сайта Сдам ГИА,'
               'полностью бесплатный и без рекламы. Бот разрабатывается на некоммерческой '
               'основе.\n'
               '\n'
               'Дорогие друзья! 🌟\n'
               'Сердечно поздравляю с превосходным достижением - более 100 пользователей уже пользуются моим Telegram ботом! 🎉\n'
               'Это невероятно важный момент для меня, и я хочу выразить огромную благодарность каждому из вас за вашу поддержку и доверие. 💖\n'
               'Ваша активность и отзывчивость вдохновляют меня на еще большие свершения! 🚀\n'
               'Спасибо, что делаете меня сильнее каждый день! 💪\n'
               '\n'
               f'Обратная связь: /support')

    await message.answer_photo(assets.header, content,
                               reply_markup=get_keyboard(message.from_user.id))
