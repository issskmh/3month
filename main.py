import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


names = ["Алексей", "Мария", "Иван", "Елена", "Сергей"]


unique_users = set()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id

    unique_users.add(user_id)
    unique_count = len(unique_users)
    await message.reply(f"Привет, {message.from_user.first_name}! Наш бот обслуживает уже {unique_count} пользователя(ей).")


@dp.message(Command("myinfo"))
async def myinfo_command(message: types.Message):
    user_info = (
        f"Ваш id: {message.from_user.id}\n"
        f"Ваше имя: {message.from_user.first_name}\n"
        f"Ваш никнейм: @{message.from_user.username}" if message.from_user.username else "Нет никнейма"
    )
    await message.reply(user_info)


@dp.message(Command("random"))
async def random_command(message: types.Message):
    random_name = random.choice(names)
    await message.reply(f"Случайное имя: {random_name}")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
