from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

review_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    user_contact = State()
    date_visit = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    finish = State()

@review_router.callback_query(F.data == "review")
async def start_review(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(RestourantReview.name)
    await callback_query.message.answer("Как вас зовут?")

@review_router.message(RestourantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestourantReview.user_contact)
    await message.answer("Введите ваш номер телефона или инстаграм:")

@review_router.message(RestourantReview.user_contact)
async def process_user_contact(message: types.Message, state: FSMContext):
    await state.update_data(user_contact=message.text)
    await state.set_state(RestourantReview.date_visit)
    await message.answer("Введите дату вашего визита (например, 2024-11-11):")

@review_router.message(RestourantReview.date_visit)
async def process_date_visit(message: types.Message, state: FSMContext):
    await state.update_data(date_visit=message.text)
    await state.set_state(RestourantReview.food_rating)
    await message.answer("Введите оценку еды (1 - очень плохо, 5 - замечательно):")

@review_router.message(RestourantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=int(message.text))
        await state.set_state(RestourantReview.cleanliness_rating)
        await message.answer("Введите оценку чистоты (1 - очень плохо, 5 - замечательно):")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки еды.")


@review_router.message(RestourantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=int(message.text))
        await state.set_state(RestourantReview.extra_comments)
        await message.answer("Пожалуйста, добавьте дополнительные комментарии или жалобы, если они есть:")
    else:
        await message.answer("Оценка чистоты должна быть числом от 1 до 5. Пожалуйста, попробуйте снова.")


@review_router.message(RestourantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await state.set_state(RestourantReview.finish)


    user_data = await state.get_data()
    review_text = (
        f"Спасибо за ваш отзыв!\n\n"
        f"Имя: {user_data['name']}\n"
        f"Контакт: {user_data['user_contact']}\n"
        f"Дата визита: {user_data['date_visit']}\n"
        f"Оценка еды: {user_data['food_rating']}\n"
        f"Оценка чистоты: {user_data['cleanliness_rating']}\n"
        f"Комментарий: {user_data['extra_comments']}"
    )
    await message.answer(review_text)
    await state.update_data(review_given=True)
    await state.clear()
