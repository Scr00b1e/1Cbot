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
    result = State()

#get_image
def getImage(user_data):
    try:
        img = Image.open(user_data['chosen_image'])
        result = pytesseract.image_to_string(img, lang='rus+eng')

        print(result)
        return result

    except Exception as e:
        print(f"Chosen image type: {type(user_data['chosen_image'])}")
        return f"❌ Ошибка {str(e)}"

@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='Отправьте картинку', reply_markup=kb.report_keyboard)
    await state.set_state(ImgHandle.image)

@router.message(ImgHandle.image, F.document)
async def handle_image(message: Message, state: FSMContext):
    await state.update_data(chosen_image=message.document)
    #user_data = await state.get_data()
    #respond_text = getImage(user_data)
    #await message.answer(respond_text)
    await message.answer(text='Do you like the result? \n\n'
    'If you don\'t then you can send it again', reply_markup=kb.options_keyboard)
    await state.set_state(ImgHandle.result)

#image liked
@router.callback_query(F.data == 'yes')
async def handle_accept(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_result=callback.message.text.lower())
    await callback.message.answer(text='Aight brow then we bounce', reply_markup=kb.report_keyboard)
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