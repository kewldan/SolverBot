from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config
from database import User

management_router = Router()


@management_router.message(F.text, F.text == '💻 Администрирование', F.from_user.id.in_(config.bot.owners))
async def on_management_button(message: Message):
    builder = InlineKeyboardBuilder()

    builder.button(text='📢 Рассылка', callback_data='distribute')
    builder.button(text='🧑‍🎓 Пользователи', callback_data='users')
    builder.button(text='📈 График', callback_data='graph')

    builder.adjust(1, repeat=True)

    if type(message) is Message:
        # noinspection PyTypeChecker
        func = message.answer
    else:
        # noinspection PyTypeChecker
        func = message.message.edit_text

    me = await message.bot.get_me()

    users = await User.count()
    blocked = await User.find(User.blocked == True).count()

    await func(
        text=f'<b>Администрирование @{me.username}</b>\n'
             '\n'
             f'Пользователей: {users}\n'
             f'Заблокированные: {blocked} ({round(blocked / users * 100, 1)}%)\n'
             + (
                 '\n⚠️ <b>ВКЛЮЧЕН ТЕСТОВЫЙ РЕЖИМ</b> ⚠️' if config.bot.debug else ''),
        reply_markup=builder.as_markup())
