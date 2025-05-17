# plgs/chat_info.py

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.async_session import async_session
from db.crud import get_channel_by_id
from utils.logger import logger


@Client.on_callback_query(filters.regex(r"^get_info_channel:[\w\-]+$"))
async def channel_info_handler(client: Client, callback: CallbackQuery):
    logger.info(f"Обработчик канала: нажата кнопка {callback.data}")

    try:
        channel_id = int(callback.data.split(":")[1])
        logger.info(f"Распознан channel_id: {channel_id}")
    except (IndexError, ValueError):
        logger.error(f"Ошибка парсинга channel_id из callback_data: {callback.data}")
        await callback.answer("Ошибка формата callback_data", show_alert=True)
        return

    user_id = callback.from_user.id

    async with async_session() as session:
        channel = await get_channel_by_id(session, channel_id)

        if not channel:
            logger.warning(f"Канал с ID {channel_id} не найден в базе")
            await callback.answer("Канал не найден.", show_alert=True)
            return

        logger.info(f"Канал найден: {channel.title} (ID: {channel.channel_id})")

    text = (
        f"✅ Канал <b>{channel.title}</b> успешно подключен.\n"
        f"<code>channel_id: {channel.channel_id}</code>\n"
        f"start_count_subs: {channel.start_count_subs}"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Парсинг", callback_data=f"parsing:{channel.channel_id}")],
        [InlineKeyboardButton("Отчёт", callback_data=f"report:{channel.channel_id}")],
        [InlineKeyboardButton("Главное меню", callback_data="start")]
    ])

    await callback.message.edit_text(text, reply_markup=buttons)
    await callback.answer()
