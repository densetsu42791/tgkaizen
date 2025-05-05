from pyrogram import Client
from db.database import async_session
from db.crud import get_user_by_id, create_user
from pyrogram.types import User as PyroUser
from datetime import datetime

async def check_or_create_user(client: Client, user_id: int) -> str:
    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if user:
            return f"👤 User_id: {user.user_id}\n📢 Channel_id: {user.channel_id}"
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

            new_user = await create_user(user_data, session)
            return f"✅ Новый пользователь добавлен\nUser_id: {new_user.user_id}"
