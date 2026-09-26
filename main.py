import asyncio
from aiogram import Dispatcher, Bot, F
from dotenv import load_dotenv
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
bot = Bot(os.getenv("token_bot"))
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())