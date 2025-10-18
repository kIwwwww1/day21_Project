from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from sqlalchemy.orm import Session

# 

from database.database import User, MainСity, engine

user_router = Router()

@user_router.message(CommandStart())
async def command_start(message: types.Message):
    with Session(engine) as session:
        user = session.query(User).filter_by(user_id=message.from_user.id).first()
        if user is not None:
            await message.answer(f'И сново привет {message.from_user.username}')
        else:
            user_id, user_name = message.from_user.id, message.from_user.username
            session.add(User(user_id=user_id, user_name=user_name))
            session.commit()
            await message.answer(f'Привет {user_name}')