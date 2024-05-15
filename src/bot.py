from kwldn_bot import XMultiBot, XBot
from kwldn_bot.modules.error_handler import add_to_router

from config import config
from handlers import commands_router, callbacks_router, buttons_router
from middlewares import UserFetchMiddleware

if config.bot.debug:
    bot = XBot(config.bot.token)
else:
    bot = XMultiBot(config.bot.token, config.web.base_url, config.web.port)

add_to_router(bot.router, bot.main_bot, config.bot.owners, 'https://t.me/kwld_manager')
# bot.router.message.middleware(PauseMiddleware())
# bot.router.callback_query.middleware(PauseMiddleware())
bot.router.message.middleware(UserFetchMiddleware())
bot.router.callback_query.middleware(UserFetchMiddleware())

bot.router.include_routers(commands_router, callbacks_router, buttons_router)
