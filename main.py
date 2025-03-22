import logging
import asyncio
# import requests
# import base64
from aiogram import Bot, Dispatcher

from config import TGTOKEN
from app.handlers import router

bot = Bot(TGTOKEN)
dp = Dispatcher()

async def main():
    await bot.delete_webhook()

    dp.include_router(router)
    await dp.start_polling(bot)

# async def get_report1c():
#     url = "http://localhost/base/hs/tg/report"

#     username = "Админ"
#     password = '12345'
#     credentials = f"{username}:{password}".encode("utf-8")
#     encoded_credentials = base64.b64encode(credentials).decode("utf-8")

#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Content-Type": "application/json"
#     }

#     try:
#         responce = requests.post(url, headers=headers)

#         if responce.status_code == 200:
#             try:
#                 data = responce.json()

#                 if not isinstance(data, list):
#                     return f"Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

#                 table = "Отчет из 1С:\n"
#                 table += "```\n{:25} {:10}\n".format("Клиент", "Сумма")
#                 table += "-" * 38 + "\n"

#                 for row in data:
#                     table += "{:25} {:10.2f}\n".format(
#                     row.get("Клиент", ""), row.get("Сумма", 0)
#                 )

#                 table += "```"
#                 return table

#             except Exception as e:
#                 return f"Ошибка при подключении к 1С"
        
#         else: 
#             return f"Ошибка от 1С: {responce.status_code}\n\n"

#     except Exception as e:
#         return f"Ошибка при подключении к 1С"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')