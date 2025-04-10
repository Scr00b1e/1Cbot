from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()

available_food_names = ["Sushi", "Spaghetti", "Khachapuri"]
available_food_sizes = ["Small", "Middle", "Large"]

class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

@router.message(Command('food'))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Choose food:")
    await state.set_state(OrderFood.choosing_food_name)

@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Thanks. Now, please choose the size:"
    )
    await state.set_state(OrderFood.choosing_food_size)

@router.message(StateFilter('OrderFood:choosing_food_name'))
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text='I do not know this food.\n\n'
        "Choose the correct food please"
    )

@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"You chose size {message.text.lower()} of the food {user_data['chosen_food']}"
    )
    await state.clear()

@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text='I do not know this size of portion.\n\n'
        'Choose the right size please'
    )