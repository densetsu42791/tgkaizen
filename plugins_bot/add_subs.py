from pyrogram import Client, filters
from pyrogram.types import Message
from db.database import async_session
from db.crud import get_user_by_id
from src.channels import fetch_and_store_subscribers
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("add_subs") & filters.private)
async def cmd_add_subs(client: Client, message: Message):
    user_id = message.from_user.id

    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if not user or not user.channel_id:
            await message.reply_text("❌ Сначала добавьте канал командой /add_channel.")
            return

        try:
            await fetch_and_store_subscribers(client, user.channel_id, session)
            await message.reply_text("✅ Подписчики успешно добавлены в БД.")
        except PermissionError as e:
            await message.reply_text(str(e))
        except Exception as e:
            logger.exception("Ошибка при добавлении подписчиков:")
            await message.reply_text("⚠️ Ошибка при получении подписчиков.")
