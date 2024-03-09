from kwldn_bot import XMultiBot, XBot
from kwldn_bot.modules.error_handler import add_to_router

from config import config
from handlers.buttons import buttons_router
from handlers.callback import callbacks_router
from handlers.commands import commands_router
from middlewares.user_fetch import UserFetchMiddleware

if config.bot.debug:
    bot = XBot(config.bot.token)
else:
    bot = XMultiBot(config.bot.token, config.web.base_url, config.web.port)

add_to_router(bot.router, bot.main_bot, config.bot.owners, 'https://t.me/kwld_manager')
bot.router.message.middleware(UserFetchMiddleware())
bot.router.callback_query.middleware(UserFetchMiddleware())

bot.router.include_router(commands_router)
bot.router.include_router(callbacks_router)
bot.router.include_router(buttons_router)
