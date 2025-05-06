from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, ChannelInvalid, UserNotParticipant, RPCError, ChatAdminRequired

from db.database import async_session
from db.crud import get_user_by_id, update_user_channel_id, create_channel, get_channel_by_id, add_subscriber

from src.user_state import waiting_channel
from datetime import datetime, timezone
import logging


logger = logging.getLogger(__name__)


async def process_channel_addition(client: Client, user_id: int, command_call=False, message: Message = None) -> str:
    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if not user:
            return "Вы не зарегистрированы. Сначала нажмите /start."

        existing_channel = user.channel_id and await get_channel_by_id(user.channel_id, session)
        if command_call:
            if existing_channel:
                return f"📢 Канал уже добавлен: {user.channel_id}"
            waiting_channel[user_id] = True
            return "📩 Перешлите сообщение из канала."


        chat = message.forward_from_chat
        

        try:
            full_chat = await client.get_chat(chat.id)
            if full_chat.type != ChatType.CHANNEL:
                return "❌ Это не канал."

            member = await client.get_chat_member(chat.id, client.me.id)
            privileges = getattr(member, "privileges", None)
            if privileges is None or not privileges.can_post_messages:
                return "❌ У бота нет прав администратора в канале. Проверьте, что вы выдали все права."

        except (UserNotParticipant, ChatType, ChannelInvalid, PeerIdInvalid) as e:
            logger.warning(f"Ошибка при проверке канала: {e}")
            return {
                UserNotParticipant: "❌ Бот не добавлен в канал. Добавьте его вручную перед добавлением.",
                ChannelInvalid: "❌ Канал недоступен или не существует.",
                PeerIdInvalid: "❌ Некорректный ID канала. Попробуйте другое сообщение.",
            }.get(type(e), "⚠️ Произошла ошибка при проверке канала.")
        except RPCError as e:
            logger.exception(f"Непредвиденная RPC ошибка: {e}")
            return "⚠️ Произошла ошибка при подключении к Telegram. Попробуйте позже."

        # Проверка, не добавлен ли этот канал другим пользователем
        already_linked = await get_channel_by_id(full_chat.id, session)
        if already_linked:
            return f"⚠️ Канал {full_chat.id} уже добавлен другим пользователем."
        

        # Добавление канала
        channel_data = {
            "channel_id": full_chat.id,
            "title": full_chat.title,
            "username": full_chat.username if full_chat.username else "Private",
            "description": full_chat.description,
            "type_chat": full_chat.type.value,
            "invite_link": full_chat.invite_link,
            "start_count_subs": full_chat.members_count,
            "join_at": datetime.now(timezone.utc),
        }

        await create_channel(channel_data, session)
        await update_user_channel_id(user_id, chat.id, session)
        waiting_channel.pop(user_id, None)

        return f"✅ Канал {chat.id} успешно добавлен!"


async def fetch_and_store_subscribers(client: Client, channel_id: int, session):
    try:
        async for member in client.get_chat_members(channel_id):
            sub_data = {
                "user_id": member.user.id,
                "username": member.user.username,
                "first_name": member.user.first_name,
                "last_name": member.user.last_name,
                "is_bot": member.user.is_bot,
                "channel_id": channel_id,
                "join_at": datetime.now(timezone.utc),
            }
            await add_subscriber(sub_data, session)
    except ChatAdminRequired:
        raise PermissionError("❌ У бота нет прав просматривать подписчиков.")
