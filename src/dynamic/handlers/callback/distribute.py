from aiogram import F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import utils
from bot import SolveBot
from config import config
from db import database
from dynamic.handlers.callback.state_clear import get_state_clear_markup


class DistributeStates(StatesGroup):
    message = State()


@SolveBot.router.callback_query(F.data == 'distribute_confirm', F.from_user.id.in_(config['bot']['owners']))
async def on_distribute_confirm_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    max_count = await database.users.count_documents({})

    count = 0
    async for user in database.users.find():
        try:
            await SolveBot.instance.copy_message(user['id'], query.from_user.id, data['message'])
            count += 1
        except TelegramAPIError:
            pass
    await query.answer(f'Отправлено {count}/{max_count} пользователям', show_alert=True)
    await query.message.delete()
    await state.clear()


@SolveBot.router.message(StateFilter(DistributeStates.message), F.from_user.id.in_(config['bot']['owners']))
async def on_distribute_message(message: Message, state: FSMContext):
    count = await database.users.count_documents({})

    await utils.confirm_action(message, f'разослать это сообщение {count} пользователям', True, 'distribute_confirm')

    await state.set_data({'message': message.message_id})
    await state.set_state()


@SolveBot.router.callback_query(F.data == 'distribute')
async def on_distribute_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(DistributeStates.message)

    await query.message.edit_text('<b>Отправьте сообщение для рассылки</b>', reply_markup=get_state_clear_markup())
