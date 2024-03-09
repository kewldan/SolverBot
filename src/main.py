import asyncio
import logging

from kwldn_bot.database import connect

from bot import bot
from config import config
from database import User, Problem, Test

logging.basicConfig(level=logging.DEBUG if config.bot.debug else logging.WARNING)


async def main():
    await connect(config.bot.mongo, config.bot.database, [User, Problem, Test])
    await bot.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
