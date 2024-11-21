from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
from database.database import Database

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    user_contact = State()
    date_visit = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    finish = State()

def rating_keyboard():
    buttons = [[KeyboardButton(text=str(i)) for i in range(1, 6)]]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )




@review_router.callback_query(F.data == "review")
async def start_review(callback_query: CallbackQuery, state: FSMContext):
    db = Database("C:/Users/islam/PycharmProjects/month3projects/database.sqlite")
    await state.update_data(db=db)

    await state.set_state(RestaurantReview.name)
    await callback_query.message.answer("Как вас зовут?")



@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.user_contact)
    await message.answer("Введите ваш номер телефона:")

@review_router.message(RestaurantReview.user_contact)
async def process_user_contact(message: types.Message, state: FSMContext):
    await state.update_data(user_contact=message.text)
    await state.set_state(RestaurantReview.date_visit)
    await message.answer("Введите дату вашего визита (например, 2024-11-11):")

@review_router.message(RestaurantReview.date_visit)
async def process_date_visit(message: types.Message, state: FSMContext):
    try:
        date_visit = datetime.strptime(message.text, "%Y-%m-%d").date()
        today = datetime.today().date()

        if date_visit > today:
            await message.answer("Дата визита не может быть в будущем. Пожалуйста, введите корректную дату.")
        elif date_visit < today - timedelta(days=5 * 365):
            await message.answer("Дата визита не может быть старше 5 лет. Пожалуйста, введите актуальную дату.")
        else:
            await state.update_data(date_visit=str(date_visit))
            await state.set_state(RestaurantReview.food_rating)
            await message.answer(
                "Введите оценку еды (1 - очень плохо, 5 - замечательно):",
                reply_markup=rating_keyboard()
            )
    except ValueError:
        await message.answer("Пожалуйста, введите дату в формате ГГГГ-ММ-ДД, например, 2024-11-11.")

@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=int(message.text))
        await state.set_state(RestaurantReview.cleanliness_rating)
        await message.answer(
            "Введите оценку чистоты (1 - очень плохо, 5 - замечательно):",
            reply_markup=rating_keyboard()
        )
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки еды.")

@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=int(message.text))
        await state.set_state(RestaurantReview.extra_comments)
        await message.answer("Пожалуйста, добавьте дополнительные комментарии или жалобы, если они есть:")
    else:
        await message.answer("Оценка чистоты должна быть числом от 1 до 5. Пожалуйста, попробуйте снова.")

@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    user_data = await state.get_data()
    review_text = (
        f"Проверьте ваш отзыв перед отправкой:\n\n"
        f"Имя: {user_data['name']}\n"
        f"Контакт: {user_data['user_contact']}\n"
        f"Дата визита: {user_data['date_visit']}\n"
        f"Оценка еды: {user_data['food_rating']}/5\n"
        f"Оценка чистоты: {user_data['cleanliness_rating']}/5\n"
        f"Комментарий: {user_data['extra_comments']}\n\n"
        f"Подтвердите отправку."
    )
    await message.answer(review_text, reply_markup=confirm_keyboard())
    await state.set_state(RestaurantReview.finish)

def confirm_keyboard():
    buttons = [
        [KeyboardButton(text="✅ Подтвердить"), KeyboardButton(text="❌ Отменить")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

@review_router.message(RestaurantReview.finish)
async def finish_review(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    db = user_data.get('db')
    if message.text == "✅ Подтвердить":
        try:
            db.execute(
                """
                INSERT INTO reviews (user_id, name, contact_info, visit_date, food_rating, cleanliness_rating, extra_comments)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message.from_user.id,
                    user_data['name'],
                    user_data['user_contact'],
                    user_data['date_visit'],
                    user_data['food_rating'],
                    user_data['cleanliness_rating'],
                    user_data['extra_comments']
                )
            )
            await message.answer("Спасибо за ваш отзыв!", reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            await message.answer(f"Произошла ошибка при сохранении отзыва: {e}")
        await state.clear()
    elif message.text == "❌ Отменить":
        await message.answer("Отзыв отменен.", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Пожалуйста, используйте кнопки для подтверждения или отмены.")

        print ("Вас приветсвует команда создавшая этого бота для работы с ним вы можете нажать на вспомогательные кнопки или ")
