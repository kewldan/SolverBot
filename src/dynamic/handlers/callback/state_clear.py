from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import SolveBot


def get_state_clear_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='❌ Отмена', callback_data='state_clear')
    builder.adjust(1, repeat=True)
    return builder.as_markup()


@SolveBot.router.callback_query(F.data == 'state_clear')
async def on_state_clear_callback(query: types.CallbackQuery, state: FSMContext):
    await query.answer('✅ Действие отменено')
    await query.message.delete()
    await state.clear()
