from datetime import datetime, timezone
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from app.db.session import async_session
from app.db.crud import add_many_subscribers
from app.logger import logger
from app.plgs.channel_info import channel_info_handler


@Client.on_callback_query(filters.regex(r"parse_subscribers:.*"))
async def parse_subscribers_handler(client: Client, callback: CallbackQuery):
    channel_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    try:
        subscribers = []

        async for member in client.get_chat_members(channel_id):
            logger.info(f"member.user.id: {member.user.id}\n")
            sub_data = {
                "user_id": member.user.id,
                "first_name": member.user.first_name,
                "phone_number": '7777777',
                "channel_id": channel_id,  
            }
            subscribers.append(sub_data)

        async with async_session() as session:
            await add_many_subscribers(subscribers, session)
        
        await callback.message.edit_text("✅ Подписчики успешно добавлены в базу данных.")
        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка при парсинге подписчиков: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при парсинге подписчиков.")
        await callback.answer()
