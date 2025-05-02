from pyrogram import Client
from pyrogram.types import Chat
import configparser
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from db.models import Base, User, Channel
from datetime import datetime, timezone
from pyrogram.enums import ChatType


# Парсим config.ini
config = configparser.ConfigParser()
config.read("config.ini")
DB_URL = config["database"]["url"]


# Создаем движок и сессию
engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)



# Проверка Юзера
async def check_user(user_id: int, username: str, first_name: str, last_name: str):
     async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        now = datetime.now()

        if not user:
            new_user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                join_at=now,
                last_vizit=now,
            )    
            session.add(new_user)
            await session.commit()
            return None
        
        else:
            user.last_vizit = now
            channel_id = user.channel_id
            await session.commit()
            return channel_id


async def add_channel(client: Client, user_id: int, chat: Chat) -> str:
    """Добавляет канал в базу и привязывает его к пользователю. Возвращает username или 'Private'."""
    if chat.type != ChatType.CHANNEL:
        raise ValueError("Это не канал.")
    else:
        print('Это точно канал')

    if chat.username:
        channel_username = chat.username
        print('Получен username публичного канала')
        # is_private = False
    else:
        channel_username = "Private"
        # is_private = True

    # Проверка прав бота
    try:
        member = await client.get_chat_member(chat.id, client.me.id)
        if not member.privileges or not member.privileges.can_post_messages:
            raise ValueError("У бота нет прав администратора в канале.")
    except Exception:
        raise ValueError("Бот не состоит в канале или произошла ошибка.") 
     
    async with async_session() as session:
    # Добавление канала, если его нет
        channel = await session.get(Channel, chat.id)
        if channel is None:
            new_channel = Channel(
                channel_id=chat.id,
                username=channel_username,
                description=chat.description,
                start_count_subs=chat.members_count or 0,
                join_at=datetime.now()
            )
            session.add(new_channel)

        # Привязка канала к пользователю
        user = await session.get(User, user_id)
        user.channel_id = chat.id

        await session.commit()

    return channel_username




#     async with async_session() as session:
#         # Добавление канала, если его нет
#         existing_channel = await session.get(Channel, chat.id)
#         if existing_channel is None:
#             new_channel = Channel(
#                 channel_id=chat.id,
#                 username=channel_username,
#                 description=chat.description,
#                 is_private_channel=is_private,
#                 start_count_subs=chat.members_count or 0,
#                 join_at=datetime.now()
#             )
#             session.add(new_channel)

#         # Привязка канала к пользователю
#         user = await session.get(User, user_id)
#         user.channel_id = chat.id

#         await session.commit()

#     return channel_username






# async def get_user_channel(user_id):
#     async with SessionLocal() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             if user and user.channel:
#                 return user.channel
#             return None
