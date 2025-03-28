from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📊 Получить отчёт', callback_data='get_report'), 
     #InlineKeyboardButton(text='Тест', callback_data='test')
    ]
])

reports = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отчет по деньгам", callback_data="supply_order")],
    [InlineKeyboardButton(text="Отчет по кассе", callback_data="cash_order")],
    [InlineKeyboardButton(text="Отчет по остаткам товаров", callback_data="stock_order")],
    [InlineKeyboardButton(text="↩ Назад", callback_data="back")],
    [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")]
])

stocks_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Основной склад", callback_data="get_stock")]
])

report_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩ Назад", callback_data="back")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")]
    ])

settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/catalog'), 
     KeyboardButton(text='/ask')]
])