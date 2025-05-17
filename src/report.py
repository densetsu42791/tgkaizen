from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.async_session import async_session
from db.models import Subscriber
from sqlalchemy import select, and_, func
import datetime
from utils.logger import logger


async def generate_report(channel_id: int) -> str:
    today = datetime.datetime.utcnow().date()
    today_start = datetime.datetime.combine(today, datetime.time.min)
    today_end = datetime.datetime.combine(today, datetime.time.max)

    async with async_session() as session:
        current_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == channel_id,
                    Subscriber.left_at.is_(None)
                )
            )
        )
        total_now = len(current_query.scalars().all())

        subscribed_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == channel_id,
                    Subscriber.join_at >= today_start,
                    Subscriber.join_at <= today_end
                )
            )
        )
        subscribed_today = subscribed_query.scalars().all()

        unsubscribed_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == channel_id,
                    Subscriber.left_at >= today_start,
                    Subscriber.left_at <= today_end
                )
            )
        )
        unsubscribed_today = unsubscribed_query.scalars().all()

        growth_today = len(subscribed_today) - len(unsubscribed_today)

        subscriber_names = [s.first_name for s in subscribed_today if s.first_name]
        unsubscriber_names = [s.first_name for s in unsubscribed_today if s.first_name]

        msg = (
            f"📊 Автоматический отчёт по каналу ID: <b>{channel_id}</b>\n\n"
            f"👥 Подписчиков сейчас: <b>{total_now}</b>\n"
            f"📈 Подписок сегодня: <b>{len(subscribed_today)}</b>\n"
            f"📉 Отписок сегодня: <b>{len(unsubscribed_today)}</b>\n"
            f"➕ Прирост: <b>{growth_today}</b>\n\n"
        )

        if subscriber_names:
            msg += "🟢 Подписались:\n" + "\n".join([f"• {name}" for name in subscriber_names]) + "\n\n"
        if unsubscriber_names:
            msg += "🔴 Отписались:\n" + "\n".join([f"• {name}" for name in unsubscriber_names])

        return msg
