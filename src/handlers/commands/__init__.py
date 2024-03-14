from aiogram import Router

from handlers.commands.bypass import bypass_router
from handlers.commands.solve import solve_router
from handlers.commands.start import start_router
from handlers.commands.support import support_router

commands_router = Router()
commands_router.include_routers(start_router, support_router, solve_router, bypass_router)
