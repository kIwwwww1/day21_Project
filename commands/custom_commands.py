from redis import Redis
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import Session
from json import loads, dumps
# 
from database.database import User, MainСity, engine
from keyboard.reply_kb import keyboards_text
from main_func.the_weather import get_weather

class City(StatesGroup):
    wait_city = State()

redis_client = Redis() # Заменить при деплое
user_router = Router()

# Комманда /start
@user_router.message(CommandStart())
async def command_start(message: types.Message):
    try:
        with Session(engine) as session:
            user = session.query(User).filter_by(user_id=message.from_user.id).first()
            if user is not None:
                await message.answer(f'И сново привет {message.from_user.username}')
            else:
                user_id, user_name = message.from_user.id, message.from_user.username
                session.add(User(user_id=user_id, user_name=user_name))
                session.commit()
                await message.answer(f'Привет {user_name}')
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')

  
# Комманда для входа в состояние добавления города
@user_router.message(F.text == 'add_city')
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
            await state.clear()
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')


# Комманда Получить погоду моего города
@user_router.message(Command(keyboards_text.TEXT_weather))
async def to_know_weather(message: types.Message):
    try:
        with Session(engine) as session:
            _user_city = session.query(MainСity).filter_by(user_id=message.from_user.id).first()
            if _user_city is not None:
                # Выводим погоду в городе
                await message.answer(await get_weather(_user_city.city_name))
            else:
                # говорим добавить город
                await message.answer('Введи команду: "/weather"')
    except Exception as e:
        await message.answer(f'Ошибка функции {__name__}')
        print(f'Ошибка {e}')
