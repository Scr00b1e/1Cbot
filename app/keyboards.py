from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📊 Получить отчёт', callback_data='reports'), InlineKeyboardButton(text='Тест', callback_data='test')]
])

# settings = ReplyKeyboardMarkup(reply_keyboard=[
#     [KeyboardButton(text='Получить отчеты'), KeyboardButton(text='Тест')]
# ])