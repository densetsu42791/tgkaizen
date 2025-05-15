# plgs/report.py

from pyrogram import Client, filters
from pyrogram.types import Message
from db.session import async_session
from db.models import Subscriber
from sqlalchemy import select, and_, func
import datetime

CHANNEL_ID = -1001525422379  # Жёстко заданный канал

@Client.on_message(filters.command("report"))
async def report_handler(client: Client, message: Message):
    today = datetime.datetime.utcnow().date()
    today_start = datetime.datetime.combine(today, datetime.time.min)
    today_end = datetime.datetime.combine(today, datetime.time.max)

    async with async_session() as session:
        # Подсчёт текущих подписчиков (left_at is NULL)
        current_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == CHANNEL_ID,
                    Subscriber.left_at.is_(None)
                )
            )
        )
        current_subs = current_query.scalars().all()
        total_now = len(current_subs)

        # Подписались сегодня
        subscribed_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == CHANNEL_ID,
                    Subscriber.join_at >= today_start,
                    Subscriber.join_at <= today_end
                )
            )
        )
        subscribed_today = subscribed_query.scalars().all()

        # Отписались сегодня
        unsubscribed_query = await session.execute(
            select(Subscriber).where(
                and_(
                    Subscriber.channel_id == CHANNEL_ID,
                    Subscriber.left_at >= today_start,
                    Subscriber.left_at <= today_end
                )
            )
        )
        unsubscribed_today = unsubscribed_query.scalars().all()

        growth_today = len(subscribed_today) - len(unsubscribed_today)

        # Имена
        subscriber_names = [s.first_name for s in subscribed_today if s.first_name]
        unsubscriber_names = [s.first_name for s in unsubscribed_today if s.first_name]

        msg = (
            f"📊 Отчёт по каналу ID: <b>{CHANNEL_ID}</b>\n\n"
            f"👥 Подписчиков сейчас: <b>{total_now}</b>\n"
            f"📈 Подписок сегодня: <b>{len(subscribed_today)}</b>\n"
            f"📉 Отписок сегодня: <b>{len(unsubscribed_today)}</b>\n"
            f"➕ Прирост: <b>{growth_today}</b>\n\n"
        )

        if subscriber_names:
            msg += "🟢 Подписались:\n" + "\n".join([f"• {name}" for name in subscriber_names]) + "\n\n"
        if unsubscriber_names:
            msg += "🔴 Отписались:\n" + "\n".join([f"• {name}" for name in unsubscriber_names])

        await message.reply(msg)
