from aiogram import Bot, Router, types
from aiogram.filters import Command

myinfo_router = Router()

@myinfo_router.message(Command("myinfo"))
async def myinfo_command(message: types.Message):
    user_info = (
        f"Ваш id: {message.from_user.id}\n"
        f"Ваше имя: {message.from_user.first_name}\n"
        f"Ваш никнейм: @{message.from_user.username}" if message.from_user.username else "Нет никнейма"
    )
    await message.reply(user_info)

