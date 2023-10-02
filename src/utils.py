from typing import Union

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def confirm_action(data: Union[types.Message, types.CallbackQuery], description: str, warning: bool,
                         callback_data: str):
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Подтвердить', callback_data=callback_data)
    builder.button(text='❌ Отмена', callback_data='state_clear')

    if type(data) is types.Message:
        func = data.answer
    else:
        func = data.message.edit_text

    await func(
        f'Вы уверены, что хотите {description}?' + ('\n\n⚠️ Это действие необратимо' if warning else ''),
        reply_markup=builder.as_markup())
