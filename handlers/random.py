from aiogram import Router, types
from aiogram.filters import Command
import random

random_router = Router()

# Ваш словарь с рецептами
recipes = {
    "Борщ": (
        "picture/загрузка.jpg",
        "Ингредиенты: свекла, капуста, морковь, картошка, мясо.\nПриготовление:"
        " отварите мясо, добавьте овощи, варите до готовности."
    ),
    "Пельмени": (
        "picture/загрузка (1).jpg",
        "Ингредиенты: фарш, тесто, лук, специи.\nПриготовление: слепите пельмени, отварите до готовности."
    ),
    "Салат Оливье": (
        "picture/загрузка (2).jpg",
        "Ингредиенты: картошка, морковь, яйца, колбаса, горошек, "
        "майонез.\nПриготовление: нарежьте все ингредиенты, перемешайте с майонезом."
    ),
    "Окрошка":(
        "picture/sm_513506.jpg",
        "Окрошка - идеальное блюдо для жаркого летнего дня. \nПриготовим окрошку на квасе,"
        " заправим сметаной, смесью желтков и горчицы. А для сытности добавим в окрошку кусочки отварной говядины."
    )

}

@random_router.message(Command("random"))
async def random_recipe(message: types.Message):
    recipe_name = random.choice(list(recipes.keys()))
    photo_path, recipe_caption = recipes[recipe_name]


    photo = types.FSInputFile(photo_path)
    await message.reply_photo(photo=photo, caption=f"{recipe_name}:\n{recipe_caption}")
