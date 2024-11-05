from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_router = Router()


@start_router.message(Command("start"))
async def start_command(message: types.Message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Наш сайт", url="https://tinyurl.com/msrr3t47"),
            InlineKeyboardButton(text="Инстаграм профиль", url="https://tinyurl.com/7b8rm9ep")
        ]
    ])

    await message.reply("Привет! Я ваш бот. Выберите один из вариантов:", reply_markup=keyboard)

