from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram import F, Router

import app.keyboards as kb
from utils.report import get_report1c, get_cash1c, get_stock1c

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🤖 Бот запущен и готов к работе!", reply_markup=kb.settings)

@router.message(Command('catalog'))
async def get_catalog(message: Message):
    await message.answer('Выберите каталог', reply_markup=kb.main)

#test column
@router.callback_query(F.data == 'test')
async def test(callback: CallbackQuery):
    await callback.message.edit_text('Вы выбрали тест')

#reports
@router.callback_query(F.data == 'get_report')
async def handle_callback(callback: CallbackQuery):
    await callback.message.answer('Выберите отчеты', reply_markup=kb.reports)
    await callback.message.delete()

@router.callback_query(F.data == 'supply_order')
async def supply_order(callback: CallbackQuery):
    report_text = get_report1c()
    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data == 'cash_order')
async def test_order(callback: CallbackQuery):
    report_text = get_cash1c()
    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data == 'stock_order')
async def test_order2(callback: CallbackQuery):
    report_text = get_stock1c()
    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()
    await callback.message.delete()

#close
@router.callback_query(F.data == 'close')
async def handle_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer()
