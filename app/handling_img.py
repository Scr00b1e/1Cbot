import pytesseract
from PIL import Image
from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
router = Router()

class ImgHandle(StatesGroup):
    image = State()

#get_image
def getImage(user_data):
    try:
        img = Image.open(user_data['chosen_image'])
        result = pytesseract.image_to_string(img, lang='rus+eng')

        return result
    except Exception as e:
        return f"❌ Ошибка {str(e)}"

@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Отправьте картинку', reply_markup=kb.report_keyboard)
    await state.set_state(ImgHandle.image)

@router.message(ImgHandle.image, F.photo)
async def handle_image(message: Message, state: FSMContext):
    await state.update_data(chosen_image=message.photo)
    user_data = await state.get_data()
    respond_text = getImage(user_data)
    await message.answer(respond_text)
    await state.clear()

#reject text
@router.message(ImgHandle.image, F.text)
async def handle_image(message: Message, state: FSMContext):
    await message.answer(text='Я принимаю только картинку', reply_markup=kb.undo_keyboard)
    await state.set_state(ImgHandle.image)

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