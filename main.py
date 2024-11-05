import os
# import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import logging
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random import random_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def picture():

    await dp.start_polling(bot)

async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_router)
    await dp.start_polling(bot)




if __name__ == '__main__':
    asyncio.run(main())
