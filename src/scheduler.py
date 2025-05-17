from apscheduler.schedulers.asyncio import AsyncIOScheduler
from plgs.report import generate_report
from db.async_session import async_session
from sqlalchemy import select
from pyrogram import Client
import logging
from db.models import Channel, Subscriber

logger = logging.getLogger(__name__)

# Твой Telegram ID, куда бот будет присылать отчёт
ADMIN_ID = 123456789  # <-- Укажи здесь свой реальный Telegram ID

def start_scheduler(bot: Client):
    scheduler = AsyncIOScheduler(timezone="UTC")

    async def periodic_task():
        logger.info("✅ periodic_task вызвана")
        try:
            async with async_session() as session:
                # Допустим, в БД есть таблица subscribers, и ты хочешь взять все уникальные channel_id
                result = await session.execute(select(Channel.channel_id).distinct())
                channel_ids = [row[0] for row in result.all()]

            for channel_id in channel_ids:
                try:
                    report_msg = await generate_report(channel_id)
                    await bot.send_message(chat_id='355527991', text=report_msg)
                except Exception as e:
                    logger.error(f"Ошибка при генерации или отправке отчёта для канала {channel_id}: {e}")

        except Exception as e:
            logger.exception("Ошибка внутри планировщика")

    scheduler.add_job(periodic_task, trigger="cron", hour=10)
    scheduler.start()
