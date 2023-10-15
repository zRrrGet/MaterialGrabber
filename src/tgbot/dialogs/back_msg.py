from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def answer_back_msg(m: Message, text: str, markup: InlineKeyboardMarkup = None):
    back_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='◀ Меню', callback_data='on_start')],
    ])

    if markup:
        markup.inline_keyboard.reverse()
        back_markup.inline_keyboard.extend(markup.inline_keyboard)
        back_markup.inline_keyboard.reverse()

    await m.answer(text, reply_markup=back_markup)
