import asyncio
import logging

from kwldn_bot.database import connect

import api
from bot import bot
from db.database import User

logging.basicConfig(level=logging.DEBUG if api.config.bot.debug else logging.WARNING)


async def main():
    await connect(api.config.bot.mongo, api.config.bot.database, [User])
    await bot.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
