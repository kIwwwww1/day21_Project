from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import Session
from json import loads, dumps
# 
from database.database import User, MainСity, engine
from keyboard.reply_kb import keyboards_text, main_keyboard
from main_func.the_weather import get_weather
from config.redis_init import redis_client

class City(StatesGroup):
    wait_city = State()
    wait_new_city = State()

user_router = Router()

# Комманда /start
@user_router.message(CommandStart())
async def command_start(message: types.Message):
    try:
        with Session(engine) as session:
            user = session.query(User).filter_by(user_id=message.from_user.id).first()
            if user is not None:
                await message.answer(f'И сново привет {message.from_user.username}', reply_markup=main_keyboard)
            else:
                user_id, user_name = message.from_user.id, message.from_user.username
                session.add(User(user_id=user_id, user_name=user_name))
                session.commit()
                await message.answer(f'Привет {user_name}', reply_markup=main_keyboard)
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')

  
# Комманда для входа в состояние добавления города
@user_router.message(Command('add_city'))
async def add_city(message: types.Message, state: FSMContext):
    try:
        with Session(engine) as session:
            user_city = session.query(MainСity).filter_by(user_id=message.from_user.id).first()
            if user_city is not None:
                # Выдает данные о погоде по городу
                await message.answer(f'У вас уже есть город: "{user_city.city_name}"')    
            else:
                await message.answer('Введите ваш город')
                await state.set_state(City.wait_city)
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')


# Комманда для добавления города и выход из состояния
@user_router.message(StateFilter(City.wait_city))
async def wait_user_city(message: types.Message, state: FSMContext):
    try:
        with Session(engine) as session:
            # Добавляем город пользователя в бд
            session.add(MainСity(user_id=message.from_user.id, city_name=message.text))
            session.commit()
            await message.answer(f'Вы добавили город {message.text}')
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')
    finally: 
        await state.clear()


# Комманда Получить погоду моего города
@user_router.message(F.text == keyboards_text.TEXT_weather)
async def to_know_weather(message: types.Message):
    try:
        with Session(engine) as session:
            _user_city = session.query(MainСity).filter_by(user_id=message.from_user.id).first()
            city = redis_client.get(_user_city.city_name)
            if city:
                await message.answer(city)
            else:
                await message.answer(await get_weather(_user_city.city_name))

    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')


# Вход в состояние для смены города
@user_router.message(F.text == keyboards_text.TEXT_change)
async def change_city(message: types.Message, state: FSMContext):
    try:
        with Session(engine) as session:
            user_city = session.query(MainСity).filter_by(user_id=message.from_user.id).first()
            if user_city is not None:
                # Просим ввести новый город
                await message.answer(f'Укажите новый город')    
                await state.set_state(City.wait_new_city)
            else:
                await message.answer('Укажите город через команду /add_city')
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')


# выход из состояния смены города и смена города
@user_router.message(StateFilter(City.wait_new_city))
async def new_city(message: types.Message, state: FSMContext):
    try:
        with Session(engine) as session:
            # Добавляем город пользователя в бд
            user_city = session.query(MainСity).filter_by(user_id=message.from_user.id).first()
            user_city.city_name = message.text
            session.commit()
            await message.answer(f'Вы изменили город на: {message.text}')
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')
    finally: 
        await state.clear()

@user_router.message(F.text == keyboards_text.TEXT_profile)
async def get_user_profile(message: types.Message):
    user = redis_client.get(f'{message.from_user.id}')
    if user:
        return await message.answer(user)
    try:
        with Session(engine) as session:
            user = session.query(User).filter_by(user_id=message.from_user.id).first()
            user_profile = (
                f'id: {user.user_id} \n'
                f'Ник: {user.user_name}\n'
                f'Город: {user.user_city.city_name}'
            )
            redis_client.setex(name=f'{message.from_user.id}', time=30, value=user_profile)
            await message.answer(user_profile)

    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')
