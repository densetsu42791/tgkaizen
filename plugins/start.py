from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.crud import check_user
from pyrogram.types import CallbackQuery
from pyrogram.enums import ChatType

import logging
logger = logging.getLogger(__name__)




@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f"User {user_id} started the bot.")
    
    channel_id = await check_user(user_id, username, first_name, last_name)

    if channel_id:
        text_channel = channel_id
    else:
        text_channel = "Канал не подключен"
    
    await message.reply_text(f"Главное меню: \nUsername: {first_name} \nChannel: {text_channel}")

