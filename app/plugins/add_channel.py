from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

from app.utils.user_context import set_state, get_state, clear_state
from app.db.crud import add_channel, get_user_by_id, get_channel_by_id
from app.db.session import async_session
from app.logger import logger

from app.plugins.start import send_start_message  # Импортируем универсальную функцию


@Client.on_callback_query(filters.regex("add_channel"))
async def cb_add_channel(client: Client, callback):
    user_id = callback.from_user.id
    set_state(user_id, "waiting_for_channel")
    await callback.message.reply("Перешлите сообщение из канала")
    await callback.answer()


@Client.on_message(filters.private & filters.forwarded)
async def handle_forwarded_channel(client: Client, message: Message):
    user_id = message.from_user.id
    state = get_state(user_id)

    if state != "waiting_for_channel":
        return

    chat = message.forward_from_chat
    if not chat:
        await message.reply("❌ Не удалось распознать канал. Попробуйте ещё раз.")
        return

    try:
        full_chat = await client.get_chat(chat.id)
        if full_chat.type != ChatType.CHANNEL:
            await message.reply("❌ Это не канал.")
            return

        member = await client.get_chat_member(chat.id, client.me.id)
        privileges = getattr(member, "privileges", None)
        if privileges is None or not privileges.can_post_messages:
            await message.reply("❌ У бота нет прав администратора в канале. Проверьте, что вы выдали все права.")
            return

    except Exception as e:
        logger.error(f"Ошибка при подключении канала: {e}")
        await message.reply("❌ Ошибка при подключении канала.")
        return

    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        if not user:
            await message.reply("Сначала нажмите /start")
            return

        exists = await get_channel_by_id(session, chat.id)
        if exists:
            await message.reply(f"Канал \"{chat.title}\" уже добавлен.")
            return

        channel_data = {
            "channel_id": full_chat.id,
            "title": full_chat.title,
            "start_count_subs": full_chat.members_count,
            "user_id": user_id, 
        }

        await add_channel(session, full_chat.id, full_chat.title, user_id, full_chat.members_count)
        clear_state(user_id)

        await send_start_message(client, user_id)
