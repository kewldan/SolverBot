import json
import math
import os
import time
from typing import Optional

import aiofiles
import aiohttp
from aiohttp import ContentTypeError
from bs4 import BeautifulSoup
from pydantic import BaseModel

import api
from db.database import Problem


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
            "user": api.config.account.username,
            "password": api.config.account.password,
            "guest": False
        }) as login_request:
            try:
                login = await login_request.json()
            except ContentTypeError:
                print(await login_request.text())
                login = {'status': False}
            if login['status']:
                async with session.get(f'{hostname}/test?id={test_id}') as task_request:
                    test_soup = BeautifulSoup(await task_request.text(), 'html.parser')
                    problems = test_soup.find_all('div', class_='prob_maindiv')

                    messages: list[ProblemData] = []
                    for problem_element in problems:
                        problem_int_id = problem_element.attrs['data-id']
                        index = problem_element.attrs['data-num']
                        problem = await Problem.find_one(Problem.internal_id == problem_int_id)
                        if problem:
                            messages.append(ProblemData(index=index, solution=problem.solution or 'Нет решения',
                                                        answer=problem.answer or 'Нет ответа',
                                                        problem_id=problem.problem_id))
                        else:
                            messages.append(ProblemData(index=index, solution='Нет в базе', answer='нет',
                                                        problem_id=0))
                    return messages
