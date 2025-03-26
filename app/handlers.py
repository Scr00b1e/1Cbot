from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

import app.keyboards as kb
from app.generators import ai_generate
from utils.report import get_report1c, get_cash1c, get_stock1c

router = Router()

class Generate(StatesGroup):
    wait = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🤖 Бот запущен и готов к работе!", reply_markup=kb.settings)

@router.message(Command('catalog'))
async def get_catalog(message: Message):
    await message.answer('Выберите каталог', reply_markup=kb.main)

#chat bot
@router.message(Command('ask'))
async def ask_bot(message: Message):
    await message.answer('Вы можете спросить вопрос')


@router.message(Generate.wait)
async def generate_error(message: Message):
    await message.answer('Подождите, пока генерируется')

@router.message()
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.wait)
    response = await ai_generate(message.text)
    await message.answer(response)
    await state.clear()

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
