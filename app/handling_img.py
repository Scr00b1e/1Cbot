import pytesseract
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from PIL import Image
import pandas as pd
import os
import tempfile

from config import TGTOKEN
import app.keyboards as kb
router = Router()
bot = Bot(TGTOKEN)

class ImgHandle(StatesGroup):
    title = State()
    count = State()
    price = State()
    table = State()

def to_json(user_data):
    payload = {"Наименование": user_data['chosen_title'],
            "Количество": user_data['chosen_count'],
            "Цена": user_data['chosen_price']}
    
    return payload

def read_image(downloaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(downloaded_file.getvalue())
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    try: 
        img = Image.open(tmp_file_path)
        result = pytesseract.image_to_string(img, lang='rus')
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            return result


@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='Отправьте картинку по частям\n\n 1.Наименование номенклатуры \n 2.Количество \n 3.Цена', reply_markup=kb.report_keyboard)
    await state.set_state(ImgHandle.title)

#TITLE
@router.message(ImgHandle.title, F.photo)
async def handle_image(message: Message, state: FSMContext):

    file = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file.file_path)

    result = read_image(downloaded_file)

    await state.update_data(chosen_title=result)
    user_data = await state.get_data()
    respond_text = f'{user_data['chosen_title']}\n Теперь отправьте количество🔢'

    await message.answer(respond_text)
    await state.set_state(ImgHandle.count)

#COUNT
@router.message(ImgHandle.count, F.photo)
async def handle_image(message: Message, state: FSMContext):

    file = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file.file_path)

    result = read_image(downloaded_file)

    await state.update_data(chosen_count=result)
    user_data = await state.get_data()
    respond_text = f'{user_data['chosen_count']}\n Теперь отправьте цену💱'

    await message.answer(respond_text)
    await state.set_state(ImgHandle.price)

#PRICE
@router.message(ImgHandle.price, F.photo)
async def handle_image(message: Message, state: FSMContext):

    file = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file.file_path)

    result = read_image(downloaded_file)

    await state.update_data(chosen_price=result)
    user_data = await state.get_data()
    respond_text = f'{user_data['chosen_price']}\n\n ✅Выберите продолжить, чтобы преобразовать в таблицу'

    await message.answer(respond_text, reply_markup=kb.options_keyboard)
    await state.set_state(ImgHandle.table)

@router.message(ImgHandle.table, F.data == 'yes')
async def handle_image(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data = to_json(user_data)

    df = pd.DataFrame(data)
    
    required_columns = ["Наименование", "Количество", "Цена"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    df = df[required_columns]

    table = "📋 *Отчёт из 1С:*\n"
    table += "```\n"
    table += df.to_string(index=False)
    table += "\n```"

    await message.answer(table, reply_markup=kb.options_keyboard)
    await state.clear()

#image liked
# @router.callback_query(F.data == 'yes')
# async def handle_accept(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(text='Выберите продолжить, чтобы преоброзовать в таблицу', reply_markup=kb.report_keyboard)
#     await state.clear()

#reject text
@router.message(ImgHandle.title, F.text)
@router.message(ImgHandle.count, F.text)
@router.message(ImgHandle.price, F.text)
async def handle_image(message: Message, state: FSMContext):
    await message.answer(text='Я принимаю только картинку, начинаем все сначала', reply_markup=kb.undo_keyboard)
    await state.clear()