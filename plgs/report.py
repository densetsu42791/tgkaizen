from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.async_session import async_session
from db.models import Subscriber
from sqlalchemy import select, and_, func
import datetime
from utils.logger import logger
from src.report import generate_report


@Client.on_callback_query(filters.regex(r"^report:[\w\-]+$"))
async def report_handler(client: Client, callback: CallbackQuery):
    logger.info(f"Обработчик Report: нажата кнопка {callback.data}")

    try:
        channel_id = int(callback.data.split(":")[1])
        logger.info(f"Распознан channel_id: {channel_id}")
    except (IndexError, ValueError):
        logger.error(f"Ошибка парсинга channel_id из callback_data: {callback.data}")
        await callback.answer("Ошибка формата callback_data", show_alert=True)
        return
    
    msg = await generate_report(channel_id)
    await callback.message.reply(msg)
    

