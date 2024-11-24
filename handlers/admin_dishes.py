from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import database


admin_dishes_router = Router()



class DishFSM(StatesGroup):
    name = State()
    description = State()
    price = State()
    confirmation = State()



@admin_dishes_router.message(Command("add_dish"))
async def start_dish_addition(message: types.Message, state: FSMContext):
    await message.answer("Введите название блюда:")
    await state.set_state(DishFSM.name)


@admin_dishes_router.message(DishFSM.name)
async def set_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить описание", callback_data="skip_description")],
        ]
    )
    await message.answer("Введите описание блюда или нажмите кнопку:", reply_markup=markup)
    await state.set_state(DishFSM.description)


@admin_dishes_router.message(DishFSM.description)
async def set_dish_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену блюда (например, 250.50):")
    await state.set_state(DishFSM.price)



@admin_dishes_router.callback_query(lambda c: c.data == "skip_description")
async def skip_description(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(description=None)
    await callback_query.message.edit_text("Введите цену блюда (например, 250.50):")
    await state.set_state(DishFSM.price)


@admin_dishes_router.message(DishFSM.price)
async def set_dish_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        data = await state.get_data()


        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes")],
                [InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")],
            ]
        )
        confirmation_text = (
            f"Название: {data['name']}\n"
            f"Описание: {data['description'] or 'Нет'}\n"
            f"Цена: {data['price']} руб.\n\n"
            "Сохранить это блюдо?"
        )
        await message.answer(confirmation_text, reply_markup=markup)
        await state.set_state(DishFSM.confirmation)
    except ValueError:
        await message.answer("Цена должна быть числом. Попробуйте ещё раз.")


@admin_dishes_router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_dish(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data.split("_")[1]

    if action == "yes":
        data = await state.get_data()
        query = "INSERT INTO dishes (name, description, price) VALUES (?, ?, ?)"
        database.execute(query, (data["name"], data["description"], data["price"]))
        await callback_query.message.edit_text("Блюдо успешно добавлено!")
    elif action == "no":
        await callback_query.message.edit_text("Добавление блюда отменено.")

    await state.clear()
