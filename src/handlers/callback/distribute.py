from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from kwldn_bot.modules.state_clear import get_state_clear_markup
from kwldn_bot.utils import confirm_action

from config import config
from database import User

distribute_router = Router()


class DistributeStates(StatesGroup):
    message = State()


@distribute_router.callback_query(F.data == 'distribute_confirm', F.from_user.id.in_(config.bot.owners))
async def on_distribute_confirm_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    max_count = await User.count()

    count = 0
    async for user in User.find():
        try:
            await query.bot.copy_message(user.user_id, query.from_user.id, data['message'])
            count += 1
        except TelegramAPIError:
            pass
    await query.message.reply(f'✅ Отправлено {count}/{max_count} пользователям')
    await state.clear()


@distribute_router.message(StateFilter(DistributeStates.message), F.from_user.id.in_(config.bot.owners))
async def on_distribute_message(message: Message, state: FSMContext):
    count = await User.count()

    await confirm_action(message, f'разослать это сообщение {count} пользователям', True, 'distribute_confirm')

    await state.set_data({'message': message.message_id})
    await state.set_state()


@distribute_router.callback_query(F.data == 'distribute')
async def on_distribute_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(DistributeStates.message)

    await query.message.edit_text('<b>Отправьте сообщение для рассылки</b>', reply_markup=get_state_clear_markup())
