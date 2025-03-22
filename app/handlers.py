from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Здравствуйте, я бот по 1С!')

@router.message(Command('catalog'))
async def get_catalog(message: Message):
    await message.answer('Выберите каталог', reply_markup=kb.main)

@router.callback_query(F.data == 'reports')
async def reports(callback: CallbackQuery):
    await callback.message.edit_text('Вы выбрали отчеты')

@router.callback_query(F.data == 'test')
async def test(callback: CallbackQuery):
    await callback.message.edit_text('Вы выбрали тест')