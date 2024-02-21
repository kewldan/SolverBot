import asyncio
import html

from aiogram import Bot, types
from aiogram.exceptions import AiogramError
from kwldn_bot.utils import get_timestamp

import api
import solver
from db.database import User


async def notify(bot: Bot, identity: str, owner: int, solved: int, test_url: str, timestamp: str, loaded: bool):
    try:
        await bot.send_message(owner,
                               f'🔔 Пользователь {identity}'
                               f' решил свой {solved + 1} '
                               f'<a href=\"{test_url}\">вариант</a> | '
                               f'{"Загружен" if loaded else "Решен"} <code>{timestamp}</code>')
    except AiogramError:
        pass


async def send_solution(bot: Bot, from_user: types.User, user: User, hostname: str, test_id: str):
    loading = await bot.send_message(from_user.id, '⏱️ Загрузка ответов...')

    test_url = f'{hostname}/test?id={test_id}'

    response = f'<b>💎 Ваш <a href=\"{test_url}\">вариант</a> [<code>{test_id}</code>] решён:</b>\n\n'
    test = await solver.get_test(hostname, test_id)
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
            await bot.send_message(from_user.id, response)
            response = ''
        if len(problem_data) <= 4000:
            response += problem_data

    if len(response) > 0:
        await bot.send_message(from_user.id, response)

    user.solved += 1

    tasks = [bot.send_message(from_user.id, answers_text),
             user.save(),
             bot.edit_message_text(f'✅ Вариант {"загружен" if test.loaded else "решен"} <code>{timestamp}</code>',
                                   from_user.id, loading.message_id)]

    if from_user.username:
        identity = html.escape(f'@{from_user.username}')
    else:
        identity = f'[<code>{from_user.id}</code>]'

    for owner in api.config.bot.owners:
        tasks.append(notify(bot, identity, owner, user.solved, test_url, timestamp, test.loaded))

    await asyncio.gather(*tasks)
