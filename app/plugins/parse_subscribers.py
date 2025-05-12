from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from app.db.session import async_session
from app.db.crud import add_subscriber
from app.logger import logger


@Client.on_callback_query(filters.regex(r"parse_subscribers:(\d+)"))
async def parse_subscribers_handler(client: Client, callback: CallbackQuery):
    channel_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    try:
        members = []
        async for member in client.get_chat_members(channel_id):
            members.append(member)

        async with async_session() as session:
            for member in members:
                await add_subscriber(session, channel_id, member.user)

        await callback.message.edit_text("✅ Подписчики успешно добавлены в базу данных.")
        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка при парсинге подписчиков: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при парсинге подписчиков.")
        await callback.answer()
