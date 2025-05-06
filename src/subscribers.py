from datetime import datetime, timezone

from pyrogram import Client
from pyrogram.types import ChatMember

from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import add_many_subscribers


async def fetch_and_store_subscribers(client: Client, channel_id: int, session):
    async for member in client.get_chat_members(channel_id):
        sub_data = {
            "user_id": member.user.id,
            "username": member.user.username,
            "first_name": member.user.first_name,
            "last_name": member.user.last_name,
            "is_bot": member.user.is_bot,
            "channel_id": channel_id,
            "join_at": datetime.now(timezone.utc),
        }
        await add_many_subscribers(sub_data, session)
        
