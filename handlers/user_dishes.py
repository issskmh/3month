from aiogram import Router, types
from aiogram.filters import Command
from config import database

user_dishes_router = Router()

@user_dishes_router.message(Command("menu"))
async def show_menu(message: types.Message):
    query = "SELECT name, description, price FROM dishes"
    dishes = database.fetch(query)


    if not dishes:
        await message.answer("Меню пока пусто. Пожалуйста, добавьте блюда.")
    else:

        menu = "📋 *Меню*:\n\n"
        for dish in dishes:
            name, description, price = dish
            menu += f"🍽️ *{name}*\n"
            menu += f"📖 {description or 'Нет описания'}\n"
            menu += f"💰 {price:.2f} руб.\n\n"

        await message.answer(menu, parse_mode="Markdown")
