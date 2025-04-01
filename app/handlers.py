from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

import app.keyboards as kb
from app.generators import ai_generate
from utils.report import get_report1c, get_cash1c, get_stock1c, send_stock, fetch_json

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
async def cash_order(callback: CallbackQuery):
    report_text = get_cash1c()
    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data == 'stock_order')
async def stock_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text="Выберите склады", 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.stocks_keyboard)
    await callback.answer()

#send stock
@router.callback_query(F.data.startswith("select_"))
async def send_stocks(callback: CallbackQuery):
    await callback.message.delete()
    
    index_str = callback.data.replace("select_", "")
    
    if not index_str.isdigit():
        await callback.message.answer("❌ Неверный формат выбора")
        return

    index = int(index_str)
    data = fetch_json()
    if not isinstance(data, list) or index >= len(data):
        await callback.message.answer("⚠️ Не удалось найти склад")
        return
    
    stock_name = data[index]["Наименование"]

    response = send_stock(stock_name)
    report_text = get_stock1c()

    if response.status_code == 200:
        await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    else:
        await callback.message.answer(f"⚠️ Ошибка от 1С ({response.status_code}):\n{response.text}")
    
    await callback.answer()

#back
@router.callback_query(F.data == 'back')
async def handle_close(callback: CallbackQuery):
    await callback.message.answer("Выберите каталог",reply_markup=kb.main)

#close
@router.callback_query(F.data == 'close')
async def handle_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer()
