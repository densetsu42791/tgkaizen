from db.database import async_session
from db.models import Base, User, Channel
from sqlalchemy import select
from datetime import datetime, timezone
from pyrogram.types import Chat
from pyrogram import Client
from pyrogram.enums import ChatType

import logging
logger = logging.getLogger(__name__)



async def add_channel_to_user(client: Client, user_id: int, chat: Chat) -> str:
    """Добавляет канал в БД и привязывает его к пользователю"""
    channel_username = chat.username or "Private"
    async with async_session() as session:
        # Добавление канала, если его нет
        channel = await session.get(Channel, chat.id)
        if channel is None:
            channel = Channel(
                channel_id=chat.id,
                username=channel_username,
                description=chat.description,
                start_count_subs=chat.members_count or 0,
                join_at=datetime.now()
            )
            session.add(channel)

        # Обновление пользователя
        user = await session.get(User, user_id)
        if user:
            user.channel_id = chat.id

        await session.commit()
    return channel_username




async def check_user(user_id: int, username: str, first_name: str, last_name: str):
     async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        now = datetime.now()

        logger.info(f"Проверяем {first_name} в БД.")

        if not user:

            logger.info(f"Записываем {first_name} в БД.")

            new_user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                join_at=now,
                last_vizit=now,
            )    
            session.add(new_user)
            logger.info(f"{first_name} записан в БД.")
            await session.commit()
            return None
        
        else:

            logger.info(f"{first_name} уже существует в БД. Обновляем дату последнего визита")
            
            user.last_vizit = now
            channel_id = user.channel_id

            logger.info(f"Проверяем подключенный канал для {first_name}.")

            await session.commit()
            return channel_id