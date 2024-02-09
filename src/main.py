import asyncio
import logging

from bot import bot

logging.basicConfig(level=logging.DEBUG)


async def main():
    await bot.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
