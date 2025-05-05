from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.crud import check_user
from pyrogram.types import CallbackQuery
from pyrogram.enums import ChatType

from services.user_info_bot import get_info_user_with_bot
from services.user_info_userbot import get_info_user_with_userbot



import logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    # username = message.from_user.username
    # first_name = message.from_user.first_name
    # last_name = message.from_user.last_name

    logger.info(f"User {user_id} started the bot.")
    # Инфо через бот
    user_info_text = await get_info_user_with_bot(client, user_id)
    await message.reply_text(f"🔍 Информация о юзере:\n{user_info_text}")

    # Инфо через юзербот
    phone_info = await get_info_user_with_userbot(user_id)
    await message.reply_text(phone_info)

    # if channel_id:
    #     text_channel = channel_id
    # else:
    #     text_channel = "Канал не подключен"
    #await message.reply_text(f"Главное меню: \nUsername: {first_name} \nChannel: {text_channel}")
    #await message.reply_text(f"Главное меню: \n User_id: {user_id} \n Channel: ???")

