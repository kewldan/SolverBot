from re import Match

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.database import User
from formater import send_solution

solve_router = Router()


@solve_router.message(F.text.regexp(r'^\d{2,}$').as_('match'))
async def on_solve_message(message: Message, match: Match[str]):
    builder = InlineKeyboardBuilder()

    builder.button(text='🔴 Решу ЕГЭ', callback_data=f'solve_ege_{match.group(0)}')
    builder.button(text='🟡 Решу ОГЭ', callback_data=f'solve_oge_{match.group(0)}')
    # builder.button(text='🟢 Решу ВПР', callback_data=f'solve_vpr_{match.group(0)}')

    builder.adjust(1, repeat=True)

    await message.reply('<b>Выберите платформу</b>', reply_markup=builder.as_markup())


@solve_router.callback_query(F.data.regexp(r'^solve_([a-z]{3})_(\d{2,})$').as_('match'))
async def on_solve_platform_message(query: CallbackQuery, match: Match[str]):
    platform = match.group(1)
    number = match.group(2)

    builder = InlineKeyboardBuilder()
    if platform == 'ege':
        builder.button(text='🧑‍🏫 Математика база', callback_data=f'solve_mathb_{platform}_{number}')
        builder.button(text='🔬 Математика проф', callback_data=f'solve_math_{platform}_{number}')
    elif platform == 'oge':
        builder.button(text='🧑‍🏫 Математика', callback_data=f'solve_math_{platform}_{number}')

    builder.button(text='🧑‍💻 Информатика', callback_data=f'solve_inf_{platform}_{number}')
    builder.button(text='⚙️ Физика', callback_data=f'solve_phys_{platform}_{number}')
    builder.button(text='📚 Литература', callback_data=f'solve_lit_{platform}_{number}')
    builder.button(text='🪆 Русский', callback_data=f'solve_rus_{platform}_{number}')
    builder.button(text='🇬🇧 Английский', callback_data=f'solve_en_{platform}_{number}')
    builder.button(text='🇩🇪 Немецкий', callback_data=f'solve_de_{platform}_{number}')
    builder.button(text='🇫🇷 Французский', callback_data=f'solve_fr_{platform}_{number}')
    builder.button(text='🇪🇸 Испанский', callback_data=f'solve_sp_{platform}_{number}')
    builder.button(text='👥 Обществознание', callback_data=f'solve_soc_{platform}_{number}')
    builder.button(text='⚗️ Химия', callback_data=f'solve_chem_{platform}_{number}')
    builder.button(text='🦠 Биология', callback_data=f'solve_bio_{platform}_{number}')
    builder.button(text='💀 История', callback_data=f'solve_hist_{platform}_{number}')
    builder.button(text='🌍 География', callback_data=f'solve_geo_{platform}_{number}')

    builder.adjust(2, repeat=True)
    await query.message.edit_text('<b>Выберите предмет</b>', reply_markup=builder.as_markup())


@solve_router.callback_query(F.data.regexp(r'^solve_([a-z]{2,4})_([a-z]{3})_(\d{2,})$').as_('match'))
async def on_solve_subject_message(query: CallbackQuery, match: Match[str], user: User):
    subject = match.group(1)
    platform = match.group(2)
    number = match.group(3)

    hostname = f'https://{subject}-{platform}.sdamgia.ru'

    await send_solution(query.bot, query.from_user, user, hostname, number)
