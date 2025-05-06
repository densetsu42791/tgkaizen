from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, Channel, Subscriber
from sqlalchemy import select, update
from datetime import datetime, timezone
from db.models import Subscriber
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert


import logging
logger = logging.getLogger(__name__)


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(user_data: dict, session: AsyncSession) -> User:
    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_last_vizit(user_id: int, session: AsyncSession) -> None:
    stmt = (
        update(User)
        .where(User.user_id == user_id)
        .values(last_vizit=datetime.now(timezone.utc))
    )
    await session.execute(stmt)
    await session.commit()


async def get_channel_by_id(channel_id: int, session: AsyncSession) -> Channel | None:
    result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
    return result.scalar_one_or_none()


async def create_channel(data: dict, session: AsyncSession) -> Channel:
    channel = Channel(**data)
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


async def update_user_channel_id(user_id: int, channel_id: int, session: AsyncSession) -> None:
    await session.execute(
        update(User).where(User.user_id == user_id).values(channel_id=channel_id)
    )
    await session.commit()



async def add_many_subscribers(subs_data: list[dict], session):
    if not subs_data:
        return

    try:
        # Используем ON CONFLICT для игнорирования дубликатов
        stmt = pg_insert(Subscriber).values(subs_data)
        stmt = stmt.on_conflict_do_nothing(index_elements=['user_id', 'channel_id'])

        await session.execute(stmt)
        await session.commit()

    except IntegrityError:
        await session.rollback()