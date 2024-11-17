from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

opros_router = Router()

# fsm = finite state machine - конечный автомат
class Opros(StatesGroup):
    name = State()
    age = State()
    gender = State()
    genre = State()

@opros_router.message(Command("opros"))
async def start_opros(message: types.Message, state: FSMContext):
    await state.set_state(Opros.name)
    await message.answer("Как вас зовут?")

@opros_router.message(Opros.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Opros.age)
    await message.answer("Напишите ваш возраст:")

@opros_router.message(Opros.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Opros.gender)
    await message.answer("Напишите ваш пол")

@opros_router.message(Opros.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Opros.genre)
    await message.answer("Какой y вас любимый литературный жанр")

@opros_router.message(Opros.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("Спасибо за пройденный опрос")
    data = await state.get_data()
    print(data)
    await state.clear()