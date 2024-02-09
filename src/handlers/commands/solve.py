import html
from re import Match

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from kwldn_bot.utils import get_timestamp

import api
import solver
from db import database
from db.types.user import User

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
    test_url = f'{hostname}/test?id={number}'

    await query.answer('Загрузка ответов...')

    response = f'<b>💎 Ваш <a href=\"{test_url}\">вариант</a> [<code>{number}</code>] решён:</b>\n\n'

    test = await solver.get_test(hostname, number)
    timestamp = get_timestamp(test.solved)
    answers_text = f'<b>🥰 Краткие ответы на <a href=\"{test_url}\">вариант</a>: </b>\n\n'

    while len(test.problems):
        problem = test.problems.pop(0)
        problem_data = (
                f'<b><a href=\"{hostname}/problem?id={problem.problem_id}\">Задание</a> номер {problem.index}:</b>\n'
                '\n'
                f'<b>Решение: </b> <pre>{html.escape(problem.solution)}</pre>\n'
                + (f'<b>Ответ: </b> <code>{html.escape(problem.answer)}</code>\n' if len(problem.answer) > 0 else '') +
                '\n')

        if len(problem.answer):
            answers_text += (f'<a href=\"{hostname}/problem?id={problem.problem_id}\">Задание {problem.index}</a>: '
                             f'<code>{html.escape(problem.answer)}</code>\n')

        if len(problem_data) > 4000:
            response += (f'<b><a href=\"{hostname}/problem?id={problem.problem_id}\">Задание</a> номер '
                         f'{problem.index} слишком длинное</b>\n')
        if len(response) + len(problem_data) > 4000:  # If next problem will overflow response flush it
            await query.message.reply(response)
            response = ''
        if len(problem_data) <= 4000:
            response += problem_data

    if len(response) > 0:
        await query.message.reply(response)

    await query.message.answer(answers_text)

    await database.users.update_one({'id': user.id}, {'$inc': {'solved': 1}})

    for owner in api.config.bot.owners:
        try:
            await query.bot.send_message(owner,
                                         f'<a href=\"{query.from_user.url}\">Пользователь</a> '
                                         f'(<code>{query.from_user.username}</code>) '
                                         f'[<code>{query.from_user.id}</code>] '
                                         f'решил свой {user.solved + 1} '
                                         f'<a href=\"{test_url}\">вариант</a> | '
                                         f'{"Загружен" if test.loaded else "Решен"} <code>{timestamp}</code>')
        except AiogramError:
            pass
