from pyrogram import Client, filters
from pyrogram.types import Message
from app.src.parse import get_info_user_with_userbot
from app.logger import logger

CHANNEL_ID = -1001525422379  # замени на актуальный ID твоего канала

@Client.on_message(filters.private & filters.command("test"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} вызвал команду /test")

    try:
        result = await get_info_user_with_userbot(channel_id=CHANNEL_ID)
        await message.reply_text(result)
    except Exception as e:
        logger.exception("Ошибка при получении информации о пользователе:")
        await message.reply_text("Произошла ошибка при обработке запроса.")
