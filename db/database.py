import configparser
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from db.models import User, Base

# Парсим config.ini
config = configparser.ConfigParser()
config.read("config.ini")
DB_URL = config["database"]["url"]

# Создаем движок и сессию
engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Функция инициализации БД (создание таблиц, если нужно)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция: добавление пользователя, если его нет
async def ensure_user_exists(user_id: int, username: str, first_name: str):
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            new_user = User(user_id=user_id, username=username, first_name=first_name)
            session.add(new_user)
            await session.commit()

# Функция: проверка, привязан ли канал
async def is_channel_linked(user_id: int) -> int | None:
    async with async_session() as session:
        stmt = select(User.channel).where(User.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


