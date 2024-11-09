from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

review_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    user_contact = State()
    date_visit = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    finish = State()

@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()

    if user_data.get("review_given", False):
        await state.clear()
        await message.answer("Нельзя оставлять отзыв более одного раза.")
        return

    await state.set_state(RestourantReview.name)
    await message.answer("Как вас зовут?")

@review_router.message(RestourantReview.name)
async def user_contact(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestourantReview.user_contact)
    await message.answer("Введите ваш номер или инстаграм:")

@review_router.message(RestourantReview.user_contact)
async def date_visit(message: types.Message, state: FSMContext):
    await state.update_data(user_contact=message.text)
    await state.set_state(RestourantReview.date_visit)
    await message.answer("Введите дату вашего визита нашего заведения:")

@review_router.message(RestourantReview.date_visit)
async def food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(date_visit=message.text)
        await state.set_state(RestourantReview.food_rating)
        await message.answer("Введите оценку еды где 1 - очень плохо, 5 - замечательно")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки еды.")

@review_router.message(RestourantReview.food_rating)
async def cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=message.text)
        await state.set_state(RestourantReview.cleanliness_rating)
        await message.answer("Введите оценку чистоты заведения где 1 - очень плохо, 5 - замечательно")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки еды.")

@review_router.message(RestourantReview.cleanliness_rating)
async def extra_comments(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=message.text)
        await state.set_state(RestourantReview.extra_comments)
        await message.answer("Дополнительные комментарии/жалоба")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки чистоты.")

@review_router.message(RestourantReview.extra_comments)
async def finish(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text, review_given=True)
    await message.answer("Спасибо, ваш отзыв был успешно принят!")
    await state.clear()
