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
    stock_name  = State()
    stock_amount  = State()
    stock_price = State()

@router.callback_query(F.data == 'add_stock')
async def cmd_stock(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Наименование номенклатуры:", reply_markup=kb.undo_keyboard)
    await state.set_state(AddStock.stock_name)

@router.message(AddStock.stock_name, F.text)
async def stock_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_stock=message.text.lower())
    await message.answer(
        text="Хорошо, теперь количество номенклатуры (цифру):"
    , reply_markup=kb.undo_keyboard)
    await state.set_state(AddStock.stock_amount)

# @router.message(StateFilter('Incorrect'))
# async def stock_chosen_incorrectly(message: Message):
#     await message.answer(
#         text='Неправильное значение номенклатуры.\n\n'
#         "Введите корректные данные"
#     )

@router.message(AddStock.stock_amount, F.text)
async def amount_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_amount=int(message.text.lower()))
        await message.answer(text="Отлично, теперь напишите цену (цифру): ")
        await state.set_state(AddStock.stock_price)
    except ValueError:
        await message.answer(
        text='Я не принимаю такое количество номенклатуры.\n\n'
        'Напишите корректную цифру'
        , reply_markup=kb.undo_keyboard)
    

@router.message(AddStock.stock_price, F.text)
async def price_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_price=int(message.text.lower()))
        user_data = await state.get_data()
        respond_text = add_stock(user_data)
        await message.answer(
        # text=f'Создана номенклатура с наименованием - {user_data['chosen_stock']}\n'
        # f'Количество - {user_data['chosen_amount']}, за цену - {user_data['chosen_price']}\n\n'
        # f'Вы можете увидеть изменения в отчетах /catalog'
        text=respond_text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.report_keyboard
        )
        await state.clear()
    except ValueError:
        await message.answer(
        text='Я не принимаю такую цену номенклатуры.\n\n'
        'Напишите корректную цифру'
        , reply_markup=kb.undo_keyboard)


#CANCEL
@router.message(StateFilter(None), Command('cancel'))
@router.message(default_state, F.text.lower() == 'cancel')
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text='Нечего отменять'
    )

@router.message(Command('cancel'))
@router.message(F.text.lower() == 'cancel')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Действие отменено'
    )