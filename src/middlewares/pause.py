from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import config
from database import get_user


class PauseMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        if str(event.from_user.id) not in config.bot.owners:
            return await event.answer('''Добрый день, в связи с последней блокировкой и окончанием учебного года, то было принято решение приостановить работу бота. Вам следует готовится к экзаменам без помощи бота, они уже совсем скоро 😔

О боте узнала администрация Сдам ГИА. Извините, что возможно доставил вам неудобства. Я просто не хотел делать свое ДЗ, а также хотел помочь другим. У меня не было и мысли о таком охвате

Донатики (https://pay.cloudtips.ru/p/34002994)
Буду рад любой сумме 💋

Спасибо за участие в проекте, нас уже >4000. Удачи всем на экзаменах ❤️, целую.

@kwld_manager, даня, 25.04.2024''')

        data['user'] = await get_user(event.bot, event.from_user)

        return await handler(event, data)
