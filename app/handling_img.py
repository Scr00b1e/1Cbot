import pytesseract
from PIL import Image
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

router = Router()

#get_image
img = Image.open('test.png')
result = pytesseract.image_to_string(img, lang='rus+eng')

@router.callback_query(F.data == 'get_image')
async def get_image(callback: CallbackQuery):
    await callback.message.answer(result, parse_mode=ParseMode.MARKDOWN)