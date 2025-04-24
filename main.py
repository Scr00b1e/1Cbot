import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage

from config import TGTOKEN
from app import adding_stock, common, handling_img #, chatbot

bot = Bot(TGTOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

async def main():
    await bot.delete_webhook()

    dp.include_router(common.router)
    #dp.include_router(chatbot.router)
    dp.include_router(adding_stock.router)
    dp.include_router(handling_img.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')