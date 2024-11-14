from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


reviewed_users = set()


class RestourantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


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

@start_router.callback_query(F.data == "about")
async def send_about_info(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Мы - команда, которая создала этого бота для помощи в ресторанах!")
