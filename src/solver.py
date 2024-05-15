import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession
from kwldn_bot.utils import distribute
from pydantic import BaseModel

import bot
from config import config
from database import Problem, Test
from utils import get_url

body_pattern = re.compile(r'body(\d+)')


class ProblemData(BaseModel):
    index: int
    problem_id: str
    solution: str
    answer: str


login_request_headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Kl-Ajax-Request': 'Ajax_Request'
}

test_request_headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Dnt': '1',
    'Pragma': 'no-cache',
    'Priority': 'u=0, i',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Arch': '"x86"',
    'Sec-Ch-Ua-Bitness': '"64"',
    'Sec-Ch-Ua-Full-Version': '"124.0.6356.6"',
    'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="124.0.6356.6", "Google Chrome";v="124.0.6356.6", "Not-A.Brand";v="99.0.0.0"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Model': '""',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}


async def authenticate(session: AsyncSession, hostname: str) -> bool:
    login_request = await session.request('POST', f'{get_url(hostname)}/newapi/login', impersonate='chrome', json={
        "user": config.account.username,
        "password": config.account.password,
        "guest": False
    }, headers={**login_request_headers}, referer=get_url(hostname))

    try:
        return login_request.json()['status']
    except Exception as e:
        logging.warning('Login request returned: ' + login_request.text)
        logging.exception(e)
        await distribute(bot.bot.main_bot, config.bot.owners, '🚨 Ошибка авторизации')
        return False


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


async def get_problems_data(user_id: int, hostname: str, test_id: str) -> tuple[Test, list[ProblemData], bool]:
    test = await Test.find_one(Test.hostname == hostname, Test.test_id == test_id)

    if test:
        problems = []
        index = 1
        for internal_id in test.problems:
            problems.append(await get_problem(hostname, index, internal_id))
            index += 1
        loaded = True
    else:
        problems: list[ProblemData] = []
        async with AsyncSession() as session:
            if await authenticate(session, hostname):
                task_request = await session.request('GET', f'{get_url(hostname)}/test?id={test_id}',
                                                     impersonate='chrome',
                                                     headers={**test_request_headers}, referer=get_url(hostname))
                test_soup = BeautifulSoup(task_request.text, 'html.parser')
                blocks = test_soup.find_all('div', class_='prob_maindiv')

                internal_ids = []
                index = 1
                for problem_element in blocks:
                    problem_int_id = body_pattern.match(
                        problem_element.find('div', id=body_pattern).attrs['id']).group(1)

                    problems.append(await get_problem(hostname, index, problem_int_id))
                    internal_ids.append(problem_int_id)
                    index += 1

                test = Test(hostname=hostname, problems=internal_ids, test_id=test_id,
                            timestamp=datetime.now(),
                            user_id=user_id)
                if len(internal_ids) > 0:
                    await test.insert()
        loaded = False
    return test, problems, loaded
