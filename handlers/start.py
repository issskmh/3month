from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery  # Импортируйте CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Глобальная переменная для отслеживания пользователей, оставивших отзывы
reviewed_users = set()

# Класс для состояний сбора отзыва
class RestourantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

# Создание кнопок для команды /start
start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Наш инстаргам",
                    url="https://tinyurl.com/7b8rm9ep"
                ),
                InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://tinyurl.com/msrr3t47"
                )
            ],
            [
                InlineKeyboardButton(
                    text="О Нас",
                    callback_data="about"
                ),
                InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="review"
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)

# Обработчик для кнопки "Оставить отзыв"
@start_router.callback_query(F.data == "review")
async def review_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id in reviewed_users:
        await callback_query.message.answer("Нельзя оставлять отзыв более одного раза.")
        await state.finish()
    else:
        await callback_query.message.answer("Здравствуйте! Давайте начнем оставлять отзыв. Как вас зовут?")
        await state.set_state(RestourantReview.name)  # Устанавливаем состояние
    await callback_query.answer()  # Закрытие callback'а, чтобы кнопка не оставалась подсвеченной
