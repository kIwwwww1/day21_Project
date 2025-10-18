from os import getenv
import asyncio
import logging
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
# 
from commands.custom_commands import user_router
from database.database import create_db

load_dotenv()

TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN) # type: ignore
dp = Dispatcher()

async def main():
    print('=== Бот запущен ==='.center(80, '='))
    create_db()
    logging.basicConfig(level=logging.INFO)
    dp.include_router(user_router)
    await dp.start_polling(bot)
    print(' Бот выключен '.center(80, '='))

if __name__ == '__main__':
    asyncio.run(main())