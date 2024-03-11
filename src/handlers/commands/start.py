from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import assets
from config import config
from database import User

start_router = Router()

content = ('👋 Привет, это бот для решения вариантов с сайта Сдам ГИА,'
           'полностью бесплатный и без рекламы. Бот разрабатывается на некоммерческой '
           'основе.\n'
           '\n'
           f'Обратная связь: /support')


def get_keyboard(user_id: int):
    builder = ReplyKeyboardBuilder()

    builder.button(text='🚀 Решить')
    builder.button(text='📊 Статистика')
    if user_id in config.bot.owners:
        builder.button(text='💻 Администрирование')

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


@start_router.message(CommandStart(deep_link=True))
async def on_start_command(message: Message, user: User, command: CommandObject):
    if not user.referral:
        user.referral = command.args
        await user.save()

    if user.blocked:
        user.blocked = False
        await user.save()

    await message.answer_photo(assets.header, content,
                               reply_markup=get_keyboard(message.from_user.id))


@start_router.message(CommandStart())
async def on_start_command(message: Message, user: User):
    if user.blocked:
        user.blocked = False
        await user.save()

    await message.answer_photo(assets.header, content,
                               reply_markup=get_keyboard(message.from_user.id))
