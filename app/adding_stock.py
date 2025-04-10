from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery

from utils.report import add_stock
import app.keyboards as kb

router = Router()

class AddStock(StatesGroup):
    choosing_stock_name  = State()
    choosing_stock_amount  = State()
    choosing_stock_price = State()

#ADD STOCK
@router.callback_query(F.data == 'food')
async def add_stocks(callback: CallbackQuery):
    report_text = add_stock()

    await callback.message.answer(report_text, 
                                  parse_mode=ParseMode.MARKDOWN, 
                                  reply_markup=kb.report_keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data == 'add_stock')
async def cmd_stock(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Наименование номенклатуры:")
    await state.set_state(AddStock.choosing_stock_name)

@router.message(AddStock.choosing_stock_name, F.text)
async def stock_chosen(message: Message, state: FSMContext):
    #store data
    await state.update_data(chosen_stock=message.text.lower())
    #
    await message.answer(
        text="Хорошо, теперь количество номенклатуры"
    )
    await state.set_state(AddStock.choosing_stock_amount)

@router.message(StateFilter('Samsy'))
async def stock_chosen_incorrectly(message: Message):
    await message.answer(
        text='I do not know this stock.\n\n'
        "Choose the correct stock please"
    )

@router.message(AddStock.choosing_stock_amount, F.text)
async def amount_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_amount=message.text.lower())
    await message.answer(
        text="Отлично, теперь напишите цену: "
    )
    await state.set_state(AddStock.choosing_stock_price)

@router.message(AddStock.choosing_stock_amount)
async def amount_chosen_incorrectly(message: Message):
    await message.answer(
        text='I do not know this amount of this stock.\n\n'
        'Choose the right amount please'
    )

@router.message(AddStock.choosing_stock_price, F.text)
async def price_chosen(message: Message, state: FSMContext):
    #get data
    user_data = await state.get_data()
    #
    await message.answer(
        text=f"Вы создали номенклатуру {user_data['chosen_stock']} количество: {user_data['chosen_amount']}.\n\n"
        f"Цена: {message.text.lower()}"
    )
    await state.clear()

#CANCEL
@router.message(StateFilter(None), Command(commands=['cancel']))
@router.message(default_state, F.text.lower() == 'cancel')
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text='Нечего отменять'
    )

@router.message(Command(commands=['cancel']))
@router.message(F.text.lower() == 'cancel')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Действие отменено'
    )