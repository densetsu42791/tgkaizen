from pyrogram import Client
from db.database import async_session
from db.crud import get_user_by_id, create_user, update_user_last_vizit
from pyrogram.types import User as PyroUser
from datetime import datetime


import logging
logger = logging.getLogger(__name__)


async def check_or_create_user(client: Client, user_id: int) -> str:
    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if user:
            await update_user_last_vizit(user_id, session)
            logger.info(f"👤 Существующий пользователь: {user_id} — last_vizit обновлён")
        else:
            pyro_user: PyroUser = await client.get_users(user_id)

            user_data = {
                "user_id": pyro_user.id,
                "username": pyro_user.username,
                "first_name": pyro_user.first_name,
                "last_name": pyro_user.last_name,
                "join_at": datetime.utcnow(),
                "last_vizit": datetime.utcnow(),
                "leave_at": None,
                "channel_id": None
            }

            user = await create_user(user_data, session)
            logger.info(f"✅ Новый пользователь добавлен: {user.user_id}")
            
        return f"👤 User_id: {user.user_id}\n📢 Channel_id: {user.channel_id}"