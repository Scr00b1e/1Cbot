import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage

from config import TGTOKEN
from app import handlers, ordering_food

bot = Bot(TGTOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

async def main():
    await bot.delete_webhook()

    dp.include_router(handlers.router)
    dp.include_router(ordering_food.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')