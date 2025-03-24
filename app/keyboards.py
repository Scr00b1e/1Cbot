from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📊 Получить отчёт', callback_data='reports'), 
     InlineKeyboardButton(text='Тест', callback_data='test')]
])

report_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Обновить", callback_data="get_report")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")]
    ])

# settings = ReplyKeyboardMarkup(reply_keyboard=[
#     [KeyboardButton(text='Получить отчеты'), KeyboardButton(text='Тест')]
# ])