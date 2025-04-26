import pytesseract
from PIL import Image
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
import io

from config import TGTOKEN
import app.keyboards as kb
router = Router()
bot = Bot(TGTOKEN)

class ImgHandle(StatesGroup):
    image = State()
    result = State()

#get_image
def getImage(img_bytes):
#def getImage():
    try:
        img = Image.open(io.BytesIO(img_bytes))
        #img = Image.open('стих.png')
        result = pytesseract.image_to_string(img, lang='rus')

        #print(result)
        return f"{result} \n\n 😁Довольны результатом? \n ✅Если да, переформатирую на таблицу \n ❌Если нет, то вы можете отправить снова"

    except Exception as e:
        print(f"Chosen image type: {img_bytes}")
        return f"❌ Ошибка {str(e)}"

@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='Отправьте картинку', reply_markup=kb.report_keyboard)
    await state.set_state(ImgHandle.image)

@router.message(ImgHandle.image, F.photo)
async def handle_image(message: Message, state: FSMContext):

    file = await message.bot.get_file(message.photo[0].file_id)
    img_bytes = await message.bot.download_file(file.file_path)

    await state.update_data(chosen_image=img_bytes)
    user_data = await state.get_data()
    respond_text = getImage(user_data['chosen_image'])
    #respond_text = getImage()
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