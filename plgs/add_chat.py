from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from utils.user_context import set_state, get_state
from utils.helpers import validate_forwarded_channel
from db.crud import add_channel, get_user_by_id, get_channel_by_id
from db.async_session import async_session
from utils.logger import logger


@Client.on_callback_query(filters.regex("add_channel"))
async def cb_add_channel(client: Client, callback):
    user_id = callback.from_user.id
    set_state(user_id, "waiting_for_channel")
    await callback.message.reply("📩 Перешлите сообщение из канала.")
    await callback.answer()


@Client.on_message(filters.private & filters.forwarded)
async def handle_forwarded_channel(client: Client, message: Message):
    user = message.from_user
    user_id = user.id

    if get_state(user_id) != "waiting_for_channel":
        return

    try:
        chat = message.forward_from_chat
        error = await validate_forwarded_channel(client, chat)
        if error:
            await message.reply(error)
            return

        full_chat = await client.get_chat(chat.id)

        async with async_session() as session:
            db_user = await get_user_by_id(session, user_id)
            if not db_user:
                await message.reply("⚠️ Сначала нажмите /start.")
                return

            exists = await get_channel_by_id(session, chat.id)
            if exists:
                await message.reply(f"ℹ️ Канал \"{chat.title}\" уже добавлен.")
                return

            await add_channel(session=session, chat=full_chat, user=db_user)
            set_state(user_id, "channel_added")

            await message.reply(
                f"✅ Канал \"{chat.title}\" успешно добавлен!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Перейти к каналу", callback_data=f"get_info_channel:{chat.id}")],
                    [InlineKeyboardButton("Главное меню", callback_data="start")]
                ])
            )

    except Exception as e:
        logger.error(f"Ошибка при добавлении канала: {e}")
        await message.reply("❌ Не удалось подключить канал.")
