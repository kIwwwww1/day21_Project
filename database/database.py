from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

load_dotenv()

URL = getenv('url_db')

engine = create_engine(URL)  # type: ignore
Base = declarative_base()

class User(Base):
    
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(nullable=False)

    user_city: Mapped['MainСity'] = relationship('MainСity', back_populates='city_user',uselist=False)

class MainСity(Base):

    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True)
    city_name: Mapped[str] = mapped_column(nullable=True)

    city_user: Mapped['User'] = relationship('User', back_populates='user_city', uselist=False)

def create_db():
    Base.metadata.create_all(engine)


