import html
from re import Match

from aiogram import F
from aiogram.exceptions import AiogramError
from aiogram.types import Message

import config
import solver
from bot import SolveBot
from db import database
from db.types.user import User
from utils import get_timestamp


@SolveBot.router.message(F.text, F.text == '🧠 Решить')
async def on_solve_button(message: Message):
    await message.answer('<b>🤔 Чтобы решить вариант, отправьте ссылку боту сообщением</b>\n'
                         '\n'
                         'Например: https://oge.sdamgia.ru/test?id=54697659')


@SolveBot.router.message(F.text, F.text.regexp(r'^(https://[a-z\-]+\.sdamgia\.ru)/test\?id=(\d+)$').as_('m'))
async def on_solve_url_message(message: Message, m: Match[str], user: User):
    status_message = await message.reply('<b>Загрузка ответов...</b>')

    response = f'<b>💎 Ваш <a href=\"{m.group(0)}\">вариант</a> [<code>{m.group(2)}</code>] решён:</b>\n\n'

    test = await solver.get_test(m.group(1), m.group(2))
    timestamp = get_timestamp(test.solved)
    answers_text = f'<b>🥰 Краткие ответы на <a href=\"{m.group(0)}\">вариант</a>: </b>\n\n'

    while len(test.problems):
        problem = test.problems.pop(0)
        problem_data = (
                f'<b><a href=\"{m.group(1)}/problem?id={problem.problem_id}\">Задание</a> номер {problem.index}:</b>\n'
                '\n'
                f'<b>Решение: </b> <pre>{html.escape(problem.solution)}</pre>\n'
                + (f'<b>Ответ: </b> <code>{html.escape(problem.answer)}</code>\n' if len(problem.answer) > 0 else '') +
                '\n')

        if len(problem.answer):
            answers_text += (f'<a href=\"{m.group(1)}/problem?id={problem.problem_id}\">Задание {problem.index}</a>: '
                             f'<code>{html.escape(problem.answer)}</code>\n')

        if len(problem_data) > 4000:
            response += (f'<b><a href=\"{m.group(1)}/problem?id={problem.problem_id}\">Задание</a> номер '
                         f'{problem.index} слишком длинное</b>\n')
        if len(response) + len(problem_data) > 4000:  # If next problem will overflow response flush it
            await message.answer(response)
            response = ''
        if len(problem_data) <= 4000:
            response += problem_data

    if len(response) > 0:
        await message.answer(response)

    await message.answer(answers_text)

    await database.users.update_one({'id': user.id}, {'$inc': {'solved': 1}})

    await status_message.edit_text(f'✅ Вариант решен <code>{timestamp}</code>')

    for owner in config.config['bot']['owners']:
        try:
            await SolveBot.instance.send_message(owner,
                                                 f'<a href=\"{message.from_user.url}\">Пользователь</a> '
                                                 f'(<code>{message.from_user.username}</code>) '
                                                 f'[<code>{message.from_user.id}</code>] '
                                                 f'решил свой {user.solved + 1} '
                                                 f'<a href=\"{m.group(0)}\">вариант</a> | '
                                                 f'{"Загружен" if test.loaded else "Решен"} <code>{timestamp}</code>')
        except AiogramError:
            pass
