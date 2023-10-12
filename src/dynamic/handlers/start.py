from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import assets
import config
from bot import SolveBot


def get_keyboard(user_id: int):
    builder = ReplyKeyboardBuilder()

    builder.button(text='🧠 Решить')
    builder.button(text='⚙️ Аккаунт')
    if user_id == config.config['bot']['owner']:
        builder.button(text='💻 Администрирование')

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


@SolveBot.router.message(CommandStart())
async def on_start_command(message: Message):
    await message.answer_photo(assets.header, '🧑‍🎓 Спасибо, что пользуетесь ботом!\n'
                                              'Бот полностью бесплатный 🤑\n'
                                              '\n'
                                              f'Ваш ID в системе - <code>{message.from_user.id}</code>\n\n'
                                              f'Обратная связь @kewldan, благодарности туда же 😋',
                               reply_markup=get_keyboard(message.from_user.id))
