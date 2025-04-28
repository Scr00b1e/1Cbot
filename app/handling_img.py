import pytesseract
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
import os
from PIL import Image

from config import TGTOKEN
import app.keyboards as kb
router = Router()
bot = Bot(TGTOKEN)

class ImgHandle(StatesGroup):
    image = State()
    result = State()

@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='Отправьте картинку', reply_markup=kb.report_keyboard)
    await state.set_state(ImgHandle.image)

@router.message(ImgHandle.image, F.photo)
async def handle_image(message: Message, state: FSMContext):

    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file.file_path)

    src = 'F:/Python/1cint/images/'
    file_path = os.path.join(src, f'{file_id}.png')

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    try: 
        img = Image.open(file_path)
        resulted = pytesseract.image_to_string(img, lang='rus')
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    await state.update_data(chosen_image=resulted)
    user_data = await state.get_data()
    respond_text = user_data['chosen_image']
    
    await message.answer(respond_text, reply_markup=kb.options_keyboard)
    await state.set_state(ImgHandle.result)

#image liked
@router.callback_query(F.data == 'yes')
async def handle_accept(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_result=callback.message.text.lower())
    await callback.message.answer(text='Хорошо, обрабатываем картинку...', reply_markup=kb.report_keyboard)
    await state.clear()

#reject text
@router.message(ImgHandle.image, F.text)
async def handle_image(message: Message, state: FSMContext):
    await message.answer(text='Я принимаю только картинку', reply_markup=kb.undo_keyboard)
    await state.set_state(ImgHandle.image)