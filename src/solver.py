import json
import math
import os
import re
import time
from typing import Optional

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel

import config


class ProblemData(BaseModel):
    index: int
    problem_id: int
    solution: str
    answer: str


class TestData(BaseModel):
    solved: int
    problems: list[ProblemData]
    loaded: bool

    async def save(self, path: str):
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(self.model_dump(), ensure_ascii=False))


async def get_test(hostname: str, test_id: str) -> TestData:
    folder = hostname.removeprefix('https://').removesuffix('.sdamgia.ru')
    if not os.path.exists(f'data/solved/{folder}'):
        os.makedirs(f'data/solved/{folder}')

    path = f'data/solved/{folder}/{test_id}.json'

    if not os.path.exists(path):
        problems = await solve(hostname, test_id)
        solved = math.floor(time.time())
        test = TestData(problems=problems, solved=solved, loaded=False)
        await test.save(path)
    else:
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            read = await f.read()
            json_read = json.loads(read)
            json_read['loaded'] = True
            test = TestData(**json_read)
    return test


async def solve(hostname: str, test_id: str) -> Optional[list[ProblemData]]:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{hostname}/newapi/login', json={
            "user": config.config['api']['username'],
            "password": config.config['api']['password'],
            "guest": False
        }) as login_request:
            login = await login_request.json()
            if login['status']:
                async with session.get(f'{hostname}/test?id={test_id}') as task_request:
                    text = await task_request.text()
                    matches = re.findall(r'comments(\d+)', text)
                    index = 1
                    messages: list[ProblemData] = []

                    for problem_id in matches:
                        async with session.get(f'{hostname}/problem?id={problem_id}') as problem_request:
                            soup = BeautifulSoup(await problem_request.text(), 'html.parser')

                            probBlock = soup.find('div', {'class': 'prob_maindiv'})
                            if probBlock is None:
                                return None

                            solution, answer = {}, ''

                            try:
                                solution = {'text': probBlock.find_all('div', {'class': 'pbody'})[1].text,
                                            'images': [i['src'] for i in
                                                       probBlock.find_all('div', {'class': 'pbody'})[1].find_all('img')]
                                            }
                            except IndexError:
                                pass
                            except AttributeError:
                                pass

                            try:
                                answer = probBlock.find(
                                    'div', {'class': 'answer'}).text.replace('Ответ: ', '')
                            except IndexError:
                                pass
                            except AttributeError:
                                pass

                            messages.append(ProblemData(index=index, solution=solution["text"], answer=answer,
                                                        problem_id=problem_id))
                            index += 1
                    return messages
