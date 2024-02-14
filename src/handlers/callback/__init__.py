from aiogram import Router
from kwldn_bot.modules.state_clear import state_clear_router

from handlers.callback.distribute import distribute_router
from handlers.callback.graph import graph_router
from handlers.callback.users import users_router

callbacks_router = Router()
callbacks_router.include_router(distribute_router)
callbacks_router.include_router(state_clear_router)
callbacks_router.include_router(users_router)
callbacks_router.include_router(graph_router)
