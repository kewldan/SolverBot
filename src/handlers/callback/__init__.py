from aiogram import Router
from kwldn_bot.modules.state_clear import state_clear_router

from handlers.callback.distribute import distribute_router
from handlers.callback.graph import graph_router
from handlers.callback.users import users_router

callbacks_router = Router()
callbacks_router.include_routers(distribute_router, state_clear_router, users_router, graph_router)
