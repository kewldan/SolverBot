from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode

import config
from middlewares.user_fetch import UserFetchMiddleware


class SolveBot(Bot):
    router = Router()
    instance: Bot

    def __init__(self):
        super().__init__(config.config['bot']['token'], parse_mode=ParseMode.HTML)
        self.dp = Dispatcher()
        self.dp.include_router(SolveBot.router)

        SolveBot.router.message.middleware(UserFetchMiddleware())
        SolveBot.router.callback_query.middleware(UserFetchMiddleware())
        SolveBot.instance = self

    async def start(self):
        await self.dp.start_polling(self)
