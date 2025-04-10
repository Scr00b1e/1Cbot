from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router

from app.generators import ai_generate

router = Router()

class Generate(StatesGroup):
    wait = State()

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