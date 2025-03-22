from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить отчеты', callback_data='reports'), InlineKeyboardButton(text='Тест', callback_data='test')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Youtube', url='https://youtube.com')]])

# cars = ['Tesla', 'Mercedes', 'BMW', 'Honda']

# async def inline_cars():
#     keyboard = InlineKeyboardBuilder()
#     for car in cars:
#         keyboard.add(InlineKeyboardButton(text=car, url='https://youtube.com'))
#     return keyboard.adjust(2).as_markup()