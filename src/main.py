import asyncio
import logging
from asyncio import WindowsSelectorEventLoopPolicy

from kwldn_bot.database import connect

from bot import bot
from config import config
from database import User, Problem, Test

logging.basicConfig(level=logging.INFO if config.bot.debug else logging.WARNING)


async def main():
    await connect(config.bot.mongo, config.bot.database, [User, Problem, Test])
    await bot.start()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
