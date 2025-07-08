from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert
from db.models import User as DBUser, Channel, Subscriber, Activity, DailyMetric
from utils.logger import logger
from typing import Optional
from datetime import datetime
from pyrogram.types import User, Chat, ChatMemberUpdated
# from src.metrics import calculate_daily_metrics


# === Пользователь в БД ===

async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[DBUser]:
    result = await session.execute(select(DBUser).where(DBUser.user_id == user_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: User) -> DBUser:
    db_user = DBUser(user_id=user.id, first_name=user.first_name)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


# === Каналы ===

async def get_user_channels(session: AsyncSession, user_id: int) -> list[Channel]:
    result = await session.execute(select(Channel).where(Channel.user_id == user_id))
    return result.scalars().all()


async def get_channel_by_id(session: AsyncSession, channel_id: int) -> Optional[Channel]:
    result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
    return result.scalar_one_or_none()


async def add_channel(session: AsyncSession, chat: Chat, user: DBUser) -> Channel:
    channel = Channel(
        channel_id=chat.id,
        title=chat.title,
        username=chat.username or "private",
        user_id=user.user_id,
        start_count_subs=chat.members_count,
        type_chat=chat.type.value,
        invite_link=chat.invite_link
    )
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel




# === Подписчики ===

async def get_subscriber(session: AsyncSession, user_id: int, channel_id: int) -> Optional[Subscriber]:
    result = await session.execute(
        select(Subscriber).where(
            Subscriber.user_id == user_id,
            Subscriber.channel_id == channel_id
        )
    )
    return result.scalar_one_or_none()


async def add_subscriber(session: AsyncSession, user: User, chat: Chat, chat_member_updated: ChatMemberUpdated) -> Subscriber:
    
    existing = await session.execute(
        select(Subscriber).where(
            Subscriber.user_id == user.id,
            Subscriber.channel_id == chat.id
        )
    )
    existing_subscriber = existing.scalar_one_or_none()

    if existing_subscriber:
        # Можно обновить данные подписчика, если нужно. Например, обновить остальные поля
        # await session.commit()
        return existing_subscriber
    
    invite_link = getattr(chat_member_updated, "invite_link", None)
    invite_link_str = invite_link.invite_link if invite_link else None

    emoji_status_str = None
    if user.emoji_status is not None:
        emoji_status_str = str(user.emoji_status.custom_emoji_id) if hasattr(user.emoji_status, 'custom_emoji_id') else str(user.emoji_status)

    subscriber = Subscriber(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=getattr(user, "phone_number", None),
        is_bot=user.is_bot,
        is_self=user.is_self,
        is_contact=user.is_contact,
        is_mutual_contact=user.is_mutual_contact,
        is_deleted=user.is_deleted,
        is_verified=user.is_verified,
        is_restricted=user.is_restricted,
        is_scam=user.is_scam,
        is_fake=user.is_fake,
        is_support=user.is_support,
        is_premium=user.is_premium,
        status=chat_member_updated.new_chat_member.status.name if chat_member_updated.new_chat_member else None,
        last_online_date=user.last_online_date,
        next_offline_date=user.next_offline_date,
        code_language=user.language_code,
        emoji_status=emoji_status_str,
        dc_id=user.dc_id,
        photo_small_id = user.photo.small_file_id if user.photo else None,
        photo_small_id_unique = None,
        restrictions=str(user.restrictions) if getattr(user, "restrictions", None) else None,
        invite_link=invite_link_str,
        channel_id=chat.id,
    )

    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return subscriber



async def update_left_at(session: AsyncSession, user_id: int, channel_id: int, left_at: datetime):
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



async def add_many_subscribers(subs_data: list[dict], session: AsyncSession):
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
        import traceback
        logger.error(traceback.format_exc())
        await session.rollback()


# === МЕТРИКИ ===

# async def save_daily_metric(db: AsyncSession, channel_id: int, subscriber_count: int, date: date):
#     metric = DailyMetric(
#         channel_id=channel_id,
#         subscriber_count=subscriber_count,
#         date=date
#     )
#     db.add(metric)
#     await db.commit()
