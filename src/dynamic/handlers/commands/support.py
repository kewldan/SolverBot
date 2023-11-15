from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import SolveBot


@SolveBot.router.message(Command('support'))
async def on_support_command(message: Message):
    builder = InlineKeyboardBuilder()

    builder.button(url='https://kewldan.vercel.app/', text='🧑‍💻 Разработчик')
    builder.button(url='https://t.me/kwld_solver_manager', text='🦸 Поддержка')

    builder.adjust(1, repeat=True)

    await message.answer('Вот наши связи:\n\nПо вопросам с ботом прошу писать в поддержку ниже',
                         reply_markup=builder.as_markup())
