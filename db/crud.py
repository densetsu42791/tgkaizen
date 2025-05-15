from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert
from db.models import User, Channel, Subscriber, Activity
from utils.logger import logger
from typing import Optional
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

async def get_subscriber(session: AsyncSession, user_id: int, channel_id: int):
    result = await session.execute(
        select(Subscriber).where(
            Subscriber.user_id == user_id,
            Subscriber.channel_id == channel_id
        )
    )
    return result.scalar_one_or_none()

async def add_subscriber(session: AsyncSession, user_id: int, first_name: str, invite_link: str,
                         phone_number: str, channel_id: int):
    subscriber = Subscriber(
        user_id=user_id,
        first_name=first_name,
        invite_link=invite_link,
        phone_number=phone_number,
        channel_id=channel_id
    )
    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return subscriber  # возвращаем объект, чтобы использовать subscriber.id

async def update_left_at(session: AsyncSession, user_id: int, channel_id: int, left_at):
    await session.execute(
        update(Subscriber)
        .where(Subscriber.user_id == user_id, Subscriber.channel_id == channel_id)
        .values(left_at=left_at)
    )
    await session.commit()

async def log_subscriber_event(session: AsyncSession, subscriber_id: int, event_type: str):
    event = Activity(
        subscriber_id=subscriber_id,
        activity=event_type
    )
    session.add(event)
    await session.commit()


async def add_many_subscribers(subs_data: list[dict], session):
    if not subs_data:
        return 'NO DATA'

    try:
        stmt = pg_insert(Subscriber).values(subs_data)
        stmt = stmt.on_conflict_do_nothing(index_elements=['user_id', 'channel_id'])

        logger.info(f"stmt: {stmt}\n")

        await session.execute(stmt)
        await session.commit()

    except IntegrityError as e:
        logger.error("IntegrityError occurred")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        
        await session.rollback()