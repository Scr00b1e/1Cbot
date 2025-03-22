from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Catalog', callback_data='catalog')],
    [InlineKeyboardButton(text='Trash', callback_data='trash'), InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Youtube', url='https://youtube.com')]])

# cars = ['Tesla', 'Mercedes', 'BMW', 'Honda']

# async def inline_cars():
#     keyboard = InlineKeyboardBuilder()
#     for car in cars:
#         keyboard.add(InlineKeyboardButton(text=car, url='https://youtube.com'))
#     return keyboard.adjust(2).as_markup()