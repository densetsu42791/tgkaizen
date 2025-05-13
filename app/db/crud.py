from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Channel, Subscriber
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from app.logger import logger
from sqlalchemy.exc import IntegrityError
import traceback


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


async def add_channel(session: AsyncSession, channel_id: int, title: str, user_id: int, start_count_subs: int) -> Channel:
    channel = Channel(
        channel_id=channel_id, 
        title=title, 
        user_id=user_id, 
        start_count_subs=start_count_subs
    )
    session.add(channel)
    await session.commit()
    return channel



# --- Работа с подписчиками ---

# async def add_subscriber(session, channel_id: int, user):
#     subscriber = Subscriber(
#         channel_id=channel_id,
#         user_id=user.id,
#         first_name=user.first_name,
#         phone_number=user.phone_number,
#     )
#     session.add(subscriber)
#     await session.commit()


# async def add_many_subscribers(subs_data: list[dict], session):
#     if not subs_data:
#         return 'NO DATA'

#     try:
#         stmt = pg_insert(Subscriber).values(subs_data)
#         stmt = stmt.on_conflict_do_nothing(index_elements=['user_id', 'channel_id'])
#         logger.info(f"stmt: {stmt}\n")
#         await session.execute(stmt)
#         # result = await session.execute(stmt, params=subs_data)
#         # logger.info(f"Row count (inserted): {result.rowcount}")
#         await session.commit()

#     except IntegrityError:
#         await session.rollback()


async def add_many_subscribers(subs_data: list[dict], session):
    if not subs_data:
        return 'NO DATA'

    try:
        stmt = pg_insert(Subscriber).values(subs_data)
        stmt = stmt.on_conflict_do_nothing(index_elements=['user_id', 'channel_id'])
        logger.info(f"stmt: {stmt}\n")
        result = await session.execute(stmt, params=subs_data)
        # logger.info(f"Row count (inserted): {result.rowcount}")
        await session.commit()

    except IntegrityError as e:
        logger.error("IntegrityError occurred")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        await session.rollback()