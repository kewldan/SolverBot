import math
import time
import traceback

from aiogram import types, F
from aiogram.types import BufferedInputFile, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from bot import SolveBot

message_limit = 3970


def get_support_markup():
    builder = InlineKeyboardBuilder()

    builder.button(text='🆘 Поддержка', url='https://t.me/kewldan')
    builder.adjust(1)

    return builder.as_markup()


def get_user_markup(user_url: str):
    builder = InlineKeyboardBuilder()

    builder.button(text='👤 Пользователь', url=user_url)
    builder.adjust(1)

    return builder.as_markup()


@SolveBot.router.error(F.update.message.as_("message"))
async def error_handler(exception: types.ErrorEvent, message: Message):
    await message.reply('❌ Похоже, что-то пошло не так, репорт отправлен', reply_markup=get_support_markup())

    for admin in config.config['bot']['owners']:
        traceback_log = BufferedInputFile(traceback.format_exc().encode(),
                                          filename=f"Traceback{math.floor(time.time())}.txt")
        await SolveBot.instance.send_document(admin, traceback_log,
                                               caption=f'⚠️ Произошла ошибка при обработке сообщения от @{message.from_user.username} [<code>{message.from_user.id}</code>]!\n'
                                                       f'<pre>{message.text}</pre>',
                                               reply_markup=get_user_markup(message.from_user.url))


@SolveBot.router.error(F.update.callback_query.as_("query"))
async def error_handler(exception: types.ErrorEvent, query: CallbackQuery):
    await query.answer('❌ Похоже, что-то пошло не так, репорт отправлен', show_alert=True)

    for admin in config.config['bot']['owners']:
        traceback_log = BufferedInputFile(traceback.format_exc().encode(),
                                          filename=f"Traceback{math.floor(time.time())}.txt")
        await SolveBot.instance.send_document(admin, traceback_log,
                                               caption=f'⚠️ Произошла ошибка при обработке кнопки от @{query.from_user.username} [<code>{query.from_user.id}</code>]!\n'
                                                       f'<code>{query.data}</code>',
                                               reply_markup=get_user_markup(query.from_user.url))
