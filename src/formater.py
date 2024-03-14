import datetime
import html

from aiogram import Bot, types
from kwldn_bot.utils import distribute

import solver
from config import config
from database import User, Test
from utils import get_url


async def send_solution(bot: Bot, from_user: types.User, user: User, hostname: str, test_id: str,
                        internal_ids: list[str] | None = None):
    loading = await bot.send_message(from_user.id, '⏱️ Загрузка ответов...')
    if internal_ids is None:
        test, problems, loaded = await solver.get_problems_data(from_user.id, hostname, test_id)
    else:
        test = Test(timestamp=datetime.datetime.now(), hostname=hostname, user_id=from_user.id, test_id=test_id,
                    problems=internal_ids)
        loaded = True
        problems = []
        index = 1
        for internal_id in internal_ids:
            problems.append(await solver.get_problem(hostname, index, internal_id))
            index += 1

    if from_user.username:
        identity = html.escape(f'@{from_user.username}')
    else:
        identity = f'[<code>{from_user.id}</code>]'

    if len(problems) == 0:
        await loading.delete()
        await distribute(bot, config.bot.owners,
                         f'🚨 {identity} пытался решить <a href="{get_url(hostname)}/test?id={test_id}">вариант</a> с 0 заданий')
        return await bot.send_message(from_user.id,
                                      '<b>🚨 Не удалось решить вариант. Обратитесь в поддержку, указав вариант. Попробуйте /bypass</b>')

    url = get_url(hostname)
    test_url = f'{url}/test?id={test_id}'
    response = f'<b>💎 Ваш <a href=\"{test_url}\">вариант</a> [<code>{test_id}</code>] решён:</b>\n\n'
    timestamp = test.timestamp.strftime('%H:%M:%S %d.%m.%Y')
    answers_text = f'<b>🥰 Краткие ответы на <a href=\"{test_url}\">вариант</a>: </b>\n\n'

    for problem in problems:
        problem_data = (
                f'<b><a href=\"{url}/problem?id={problem.problem_id}\">Задание</a> номер {problem.index}:</b>\n'
                '\n'
                f'<b>Решение: </b> <pre>{html.escape(problem.solution)}</pre>\n'
                + (f'<b>Ответ: </b> <code>{html.escape(problem.answer)}</code>\n' if len(problem.answer) > 0 else '') +
                '\n')

        if len(problem.answer):
            answers_text += (f'<a href=\"{url}/problem?id={problem.problem_id}\">Задание {problem.index}</a>: '
                             f'<code>{html.escape(problem.answer)}</code>\n')

        if len(problem_data) > 4000:
            response += (f'<b><a href=\"{url}/problem?id={problem.problem_id}\">Задание</a> номер '
                         f'{problem.index} слишком длинное</b>\n')
        if len(response) + len(problem_data) > 4000:  # If next problem will overflow response flush it
            await bot.send_message(from_user.id, response)
            response = ''
        if len(problem_data) <= 4000:
            response += problem_data

    if len(response) > 0:
        await bot.send_message(from_user.id, response)

    tasks = [bot.send_message(from_user.id, answers_text),
             user.save(),
             bot.edit_message_text(f'✅ Вариант {"загружен" if loaded else "решен"} <code>{timestamp}</code>',
                                   from_user.id, loading.message_id)]

    solved = await Test.find(Test.user_id == from_user.id).count()

    await distribute(bot, config.bot.owners, f'🔔 Пользователь {identity}'
                                             f' решил свой {solved} '
                                             f'<a href=\"{test_url}\">вариант</a> c {len(problems)} заданиями',
                     tasks)
