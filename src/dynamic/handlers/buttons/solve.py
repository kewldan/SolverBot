import re
from re import Match

import aiohttp
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from bs4 import BeautifulSoup
from sdamgia import SdamGIA

import assets
import config
from bot import SolveBot


class SolveStates(StatesGroup):
    test = State()


sdam = SdamGIA()


async def get_problem(session: aiohttp.ClientSession, url: str, problem_id: str):
    async with session.get(f'{url}/problem?id={problem_id}') as request:
        soup = BeautifulSoup(await request.text(), 'html.parser')

        probBlock = soup.find('div', {'class': 'prob_maindiv'})
        if probBlock is None:
            return None

        TOPIC_ID = ' '.join(probBlock.find(
            'span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        ID = id

        CONDITION, SOLUTION, ANSWER, ANALOGS = {}, {}, '', []

        try:
            CONDITION = {'text': probBlock.find_all('div', {'class': 'pbody'})[0].text,
                         'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[0].find_all('img')]
                         }
        except IndexError:
            pass

        try:
            SOLUTION = {'text': probBlock.find_all('div', {'class': 'pbody'})[1].text,
                        'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[1].find_all('img')]
                        }
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            ANSWER = probBlock.find(
                'div', {'class': 'answer'}).text.replace('Ответ: ', '')
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            ANALOGS = [i.text for i in probBlock.find(
                'div', {'class': 'minor'}).find_all('a')]
            if 'Все' in ANALOGS:
                ANALOGS.remove('Все')
        except IndexError:
            pass
        except AttributeError:
            pass

        return {'id': ID, 'topic': TOPIC_ID, 'condition': CONDITION, 'solution': SOLUTION, 'answer': ANSWER,
                'analogs': ANALOGS}


@SolveBot.router.message(F.text, F.text == '🧠 Решить')
async def on_solve_button(message: Message):
    await message.reply_photo(assets.example, '<b>🧠 Чтобы решить вариант, отправьте ссылку боту:</b>')


@SolveBot.router.message(F.text, F.text.regexp(r'^(https://[a-z\-]+\.sdamgia\.ru)/test\?id=(\d+)$').as_('m'))
async def on_solve_url_message(message: Message, m: Match[str]):
    response = f'<b>💎 Ваш вариант [{m.group(2)}] решён:</b>\n\n'

    index = 1
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{m.group(1)}/newapi/login', json={
            "user": config.config['api']['username'],
            "password": config.config['api']['password'],
            "guest": False
        }) as request:
            login = await request.json()
            if not login['status']:
                return await message.reply('⚠️ Не удалось авторизоваться')
        async with session.get(message.text) as request:
            text = await request.text()
            matches = re.findall(r'comments(\d+)', text)
            for task_id in matches:
                task = await get_problem(session, m.group(1), task_id)
                task_solution = (f'<b>Задание номер {index} [<code>{task_id}</code>]:</b>\n'
                                 f'\n<pre>{task["solution"]["text"]} </pre>\n\n')
                if len(response) + len(task_solution) > 3900:
                    await message.answer(response)
                    response = ''
                response += task_solution
                index += 1
    if len(response) > 0:
        await message.answer(response)
