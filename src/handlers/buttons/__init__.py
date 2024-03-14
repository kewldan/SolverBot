from aiogram import Router

from handlers.buttons.encoded import encoded_router
from handlers.buttons.management import management_router
from handlers.buttons.solve import solve_router
from handlers.buttons.statistics import statistics_router

buttons_router = Router()
buttons_router.include_routers(management_router, solve_router, statistics_router, encoded_router)
