import re
from datetime import datetime

import aiohttp
from aiohttp import ContentTypeError
from bs4 import BeautifulSoup
from pydantic import BaseModel

from config import config
from database import Problem, Test

BODY_PATTERN = re.compile(r'body(\d+)')


class ProblemData(BaseModel):
    index: int
    problem_id: str
    solution: str
    answer: str


async def get_problem(hostname: str, index: int, internal_id: str):
    problem = await Problem.find_one(
        Problem.internal_id == internal_id, Problem.hostname == hostname)
    if problem:
        return ProblemData(index=index, solution=problem.solution or 'Нет решения',
                           answer=problem.answer or 'Нет ответа',
                           problem_id=problem.problem_id)
    else:
        return ProblemData(index=index, solution='Нет в базе', answer='нет',
                           problem_id=internal_id)


async def get_problems_data(hostname: str, test_id: str) -> tuple[Test, list[ProblemData], bool]:
    test = await Test.find_one(Test.hostname == hostname, Test.test_id == test_id)

    if test:
        problems = []
        index = 1
        for internal_id in test.problems:
            problems.append(await get_problem(hostname, index, internal_id))
            index += 1
        loaded = True
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://{hostname}.sdamgia.ru/newapi/login', json={
                "user": config.account.username,
                "password": config.account.password,
                "guest": False
            }) as login_request:
                try:
                    login = await login_request.json()
                except ContentTypeError:
                    print(await login_request.text())
                    login = {'status': False}
                problems: list[ProblemData] = []
                if login['status']:
                    async with session.get(f'https://{hostname}.sdamgia.ru/test?id={test_id}') as task_request:
                        test_soup = BeautifulSoup(await task_request.text(), 'html.parser')
                        blocks = test_soup.find_all('div', class_='prob_maindiv')

                        internal_ids = []
                        index = 1
                        for problem_element in blocks:
                            problem_int_id = BODY_PATTERN.match(
                                problem_element.find('div', id=BODY_PATTERN).attrs['id']).group(1)

                            problems.append(await get_problem(hostname, index, problem_int_id))
                            internal_ids.append(problem_int_id)
                            index += 1
                        test = Test(hostname=hostname, problems=internal_ids, test_id=test_id, timestamp=datetime.now())
                        await test.insert()
        loaded = False
    return test, problems, loaded
