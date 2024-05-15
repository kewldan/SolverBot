import asyncio
import logging
import platform

from kwldn_bot.database import connect

from bot import bot
from config import config
from database import User, Problem, Test

logging.basicConfig(level=logging.INFO if config.bot.debug else logging.WARNING)


async def main():
    await connect(config.bot.mongo, config.bot.database, [User, Problem, Test])
    await bot.start()


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
