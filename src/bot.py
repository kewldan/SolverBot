from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode

import config


class SolveBot(Bot):
    router = Router()
    instance: Bot

    def __init__(self):
        super().__init__(config.config['bot']['token'], parse_mode=ParseMode.HTML)
        self.dp = None

        SolveBot.instance = self

    async def start(self):
        self.dp = Dispatcher()
        self.dp.include_router(SolveBot.router)

        await self.dp.start_polling(self)
