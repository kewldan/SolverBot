from aiogram import Router

from handlers.buttons.management import management_router
from handlers.buttons.solve import solve_router
from handlers.buttons.statistics import statistics_router

buttons_router = Router()
buttons_router.include_router(management_router)
buttons_router.include_router(solve_router)
buttons_router.include_router(statistics_router)
