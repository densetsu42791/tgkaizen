from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Channel, Subscriber
from typing import Optional
from datetime import datetime


# --- Работа с пользователем ---
async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_id: int, first_name: str) -> User:
    user = User(user_id=user_id, first_name=first_name, )
    session.add(user)
    await session.commit()
    return user


# --- Работа с каналами ---
async def get_user_channels(session: AsyncSession, user_id: int) -> list[Channel]:
    result = await session.execute(select(Channel).where(Channel.user_id == user_id))
    return result.scalars().all()


async def get_channel_by_id(session: AsyncSession, channel_id: int) -> Optional[Channel]:
    result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
    return result.scalar_one_or_none()


async def add_channel(session: AsyncSession, channel_id: int, title: str, user_id: int) -> Channel:
    channel = Channel(channel_id=channel_id, title=title, user_id=user_id)
    session.add(channel)
    await session.commit()
    return channel



# --- Работа с подписчиками ---
async def get_channel_start_count(session, channel_id: int) -> int:
    result = await session.execute(
        select(func.count()).select_from(Subscriber).where(Subscriber.channel_id == channel_id)
    )
    return result.scalar()


async def add_subscriber(session, channel_id: int, user):
    subscriber = Subscriber(
        channel_id=channel_id,
        user_id=user.id,
        username=user.username,
        invite_link=user.invite_link, # Ссылка, по которой подписчик подписался
        phone_number=user.phone_number,
        
    )
    session.add(subscriber)
    await session.commit()