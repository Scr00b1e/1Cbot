from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hi, \nyour name is {message.from_user.first_name}',
                         reply_markup=kb.main)


# @router.callback_query(F.data == 'catalog')
# async def catalog(callback: CallbackQuery):
#     await callback.message.edit_text('You choose catalog', reply_markup=await kb.inline_cars())

# @router.callback_query(F.data == 'trash')
# async def trash(callback: CallbackQuery):
#     await callback.message.edit_text('You choose trash')

# @router.callback_query(F.data == 'contacts')
# async def contacts(callback: CallbackQuery):
#     await callback.message.edit_text('You choose contacts')