from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command


class RestourantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


reviewed_users = set()


def create_rating_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 6):
        keyboard.add(KeyboardButton(str(i)))
    return keyboard

def create_text_rating_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Плохо", callback_data="food_rating_1"),
        InlineKeyboardButton(text="Удовлетворительно", callback_data="food_rating_2"),
        InlineKeyboardButton(text="Хорошо", callback_data="food_rating_3"),
        InlineKeyboardButton(text="Очень хорошо", callback_data="food_rating_4"),
        InlineKeyboardButton(text="Отлично", callback_data="food_rating_5")
    )
    return keyboard


async def start_review(message: types.Message, state: FSMContext):
    if message.from_user.id in reviewed_users:
        await message.answer("Нельзя оставлять отзыв более одного раза.")
        await state.finish()
    else:
        await message.answer("Здравствуйте! Давайте начнем оставлять отзыв. Как вас зовут?")
        await RestourantReview.name.set()


async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваш номер телефона или инстаграм?")
    await RestourantReview.phone_or_instagram.set()

async def process_phone_or_instagram(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await message.answer("Дата вашего посещения (например, 2024-11-09)?")
    await RestourantReview.visit_date.set()

async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await message.answer("Как оцениваете качество еды?", reply_markup=create_text_rating_keyboard())
    await RestourantReview.food_rating.set()

async def process_food_rating(callback: types.CallbackQuery, state: FSMContext):
    food_rating = callback.data.split("_")[2]
    await state.update_data(food_rating=food_rating)
    await callback.message.answer("Как оцениваете чистоту заведения?", reply_markup=create_text_rating_keyboard())
    await RestourantReview.cleanliness_rating.set()


async def process_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
    cleanliness_rating = callback.data.split("_")[2]
    await state.update_data(cleanliness_rating=cleanliness_rating)
    await callback.message.answer("Дополнительные комментарии или жалобы?")
    await RestourantReview.extra_comments.set()

async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    user_data = await state.get_data()

    review = f"""
    Спасибо за ваш отзыв!

    Имя: {user_data['name']}
    Номер/Инстаграм: {user_data['phone_or_instagram']}
    Дата посещения: {user_data['visit_date']}
    Оценка качества еды: {user_data['food_rating']}
    Оценка чистоты: {user_data['cleanliness_rating']}
    Дополнительные комментарии: {user_data['extra_comments']}
    """

    await message.answer(review)
    reviewed_users.add(message.from_user.id)
    await state.finish()


def register_handlers_review(router: Router):
    router.message(Command("start_review"), start_review)
    router.message(RestourantReview.name, process_name)
    router.message(RestourantReview.phone_or_instagram, process_phone_or_instagram)
    router.message(RestourantReview.visit_date, process_visit_date)
    router.callback_query(lambda c: c.data.startswith('food_rating_'), process_food_rating)
    router.callback_query(lambda c: c.data.startswith('cleanliness_rating_'), process_cleanliness_rating)
    router.message(RestourantReview.extra_comments, process_extra_comments)


review_router = Router()
register_handlers_review(review_router)
