from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime
from db.database import async_session
from db.crud import (
    get_user_by_id,
    update_user_channel_id,
    create_channel,
    get_channel_by_id
)
from utils.user_state import waiting_channel
from pyrogram.errors import (
    PeerIdInvalid,
    ChannelInvalid,
    ChatAdminRequired,
    UserNotParticipant,
    ChatWriteForbidden,
    UsernameNotOccupied
)
from pyrogram.enums import ChatType

import logging
logger = logging.getLogger(__name__)


async def process_channel_addition(client: Client, user_id: int, command_call=False, message: Message = None) -> str:
    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if not user:
            return "⚠️ Вы не зарегистрированы. Сначала нажмите /start."

        if user.channel_id and command_call:
            return f"📢 Канал уже добавлен: {user.channel_id}"

        if command_call:
            waiting_channel[user_id] = True
            return "📩 Перешлите сообщение из канала."

        chat = message.forward_from_chat
        logger.info(f"✅ CHAT {chat}")

        full_chat = await client.get_chat(chat.id)
        logger.info(f"✅ FULL CHAT {full_chat}")


        


        # invite_link_ex = await client.export_chat_invite_link(chat.id) # Постоянная ссылка (бот.админ TgKaizen) https://t.me/+6-JZwkuQV6MwMmZi
        # logger.info(f"✅ INVITE LINK EXPORT {invite_link_ex}")

        if chat.type != ChatType.CHANNEL:
            return "Это не канал."

        try:
            member = await client.get_chat_member(chat.id, client.me.id)
        except UserNotParticipant:
            return "❌ Бот не добавлен в канал. Добавьте его вручную перед добавлением."
        except ChannelInvalid:
            return "❌ Канал недоступен или не существует."
        except PeerIdInvalid:
            return "❌ Некорректный ID канала. Попробуйте другое сообщение."
        except Exception as e:
            logger.exception(f"Ошибка при получении участника канала: {e}")
            return "⚠️ Произошла ошибка при проверке бота в канале. Попробуйте позже."

        privileges = getattr(member, "privileges", None)
        if privileges is None or not privileges.can_post_messages:
            return "❌ У бота нет прав администратора в канале. Проверьте, что вы выдали все права."


        # Проверка, не добавлен ли уже этот канал
        existing_channel = await get_channel_by_id(chat.id, session)
        if existing_channel:
            return f"⚠️ Канал {chat.id} уже добавлен другим пользователем."
        
        #start_count = await client.get_chat_members_count(chat.id)
        #invite_link = await client.export_chat_invite_link(chat.id)
        # print(f"InvateLink={chat.invite_link}")
        # print(f"Descript={chat.description}")

        # Добавление канала
        channel_data = {
            "channel_id": full_chat.id,
            "title": full_chat.title,
            "username": full_chat.username,
            "description": full_chat.description,
            "type_chat": full_chat.type.value,
            "invite_link": full_chat.invite_link,
            "start_count_subs": full_chat.members_count,
            "join_at": datetime.utcnow(),
        }

        await create_channel(channel_data, session)
        await update_user_channel_id(user_id, chat.id, session)

        waiting_channel.pop(user_id, None)
        logger.info(f"✅ Канал {chat.id} добавлен пользователем {user_id}")
        return f"✅ Канал {chat.id} успешно добавлен!"


