import traceback

from aiogram import types
from aiogram.exceptions import TelegramAPIError

import config
from bot import SolveBot

message_limit = 3970


@SolveBot.router.error()
async def error_handler(_: types.ErrorEvent):
    exc = traceback.format_exc()
    left = len(exc)
    i = 0
    while left > 0:
        try:
            for owner in config.config['bot']['owners']:
                await SolveBot.instance.send_message(owner,
                                                     f'<pre>{traceback.format_exc()[i:message_limit + i]}</pre>')
            i += min(message_limit, left)
            left -= min(message_limit, left)
        except TelegramAPIError:
            pass
