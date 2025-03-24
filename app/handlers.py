from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram import F, Router

import app.keyboards as kb
from utils.report import get_report1c

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🤖 Бот запущен и готов к работе!")

@router.message(Command('catalog'))
async def get_catalog(message: Message):
    await message.answer('Выберите каталог', reply_markup=kb.main)

@router.message(F.data == 'get_report')
async def handle_callback(callback: CallbackQuery):
    report_text = get_report1c
    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()

@router.message(F.data == 'close')
async def handle_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer

@router.callback_query(F.data == 'test')
async def test(callback: CallbackQuery):
    await callback.message.edit_text('Вы выбрали тест')