from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from src.parse import parsing_with_userbot
from utils.logger import logger
from plgs.chat_info import channel_info_handler

#CHANNEL_ID = -1001525422379  # TgKaizen channel

@Client.on_callback_query(filters.regex(r"^parsing:[\w\-]+$"))
async def cb_parsing(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    channel_id = int(callback.data.split(":")[1])

    logger.info(f"Пользователь {user_id} вызвал парсинг канала {channel_id}")
    await callback.answer("Запускаем парсинг...")

    try:
        result = await parsing_with_userbot(channel_id)
        await callback.message.edit_text(result)
    except Exception as e:
        logger.exception("Ошибка при получении информации о пользователе:")
        await callback.message.edit_text("Произошла ошибка при обработке запроса.")
