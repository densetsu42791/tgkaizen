from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.parse import parsing_with_userbot
from utils.logger import logger


#CHANNEL_ID = -1001525422379  # TgKaizen channel

@Client.on_callback_query(filters.regex(r"^parsing:[\w\-]+$"))
async def cb_parsing(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    channel_id = int(callback.data.split(":")[1])

    logger.info(f"Пользователь {user_id} вызвал парсинг канала {channel_id}")
    await callback.answer("Запускаем парсинг...")

    try:
        result = await parsing_with_userbot(channel_id)

    except Exception as e:
        logger.exception("Ошибка при получении информации о пользователе:")
        await callback.message.edit_text("Произошла ошибка при обработке запроса.")

    await callback.message.reply(
            f"✅ Собрано и сохранено {result} уникальных подписчиков.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Перейти к каналу", callback_data=f"get_info_channel:{channel_id}")],
                [InlineKeyboardButton("Главное меню", callback_data="start")]
            ])
        )
