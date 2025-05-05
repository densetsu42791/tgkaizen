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
        logger.info(f"Юзер {user_id} уже существует")

        if user.channel_id and command_call:
            return f"📢 Канал уже добавлен: {user.channel_id}"
        logger.info(f"Канал еще не добавлен")

        if command_call:
            waiting_channel[user_id] = True
            return "📩 Перешлите сообщение из канала."
        logger.info(f"Сообщение из канала")

        # Обработка пересланного сообщения
        if not message or not message.forward_from_chat:
            return "❌ Это не пересланное сообщение из канала. Попробуйте ещё раз."
        logger.info(f"Обработка персланного сообщения")
        chat = message.forward_from_chat
        logger.info(f"Получен чат {chat}")
        if chat.type != ChatType.CHANNEL:
            return "Это не канал."
        logger.info(f"Это канал")
        try:
            chat_info = await client.get_chat(chat.id)

            # Проверим наличие username — признак публичности
            is_private = chat_info.username is None

            # Проверим, является ли бот админом
            if not chat_info.permissions:
                return "❌ Бот не является администратором в канале. Добавьте его и дайте права администратора."

        except ChatAdminRequired:
            return "❌ Бот не является админом. Проверьте права доступа."
        except UserNotParticipant:
            return "❌ Бот не добавлен в канал. Добавьте его вручную перед добавлением."
        except (ChannelInvalid, PeerIdInvalid):
            return "❌ Канал недоступен или не существует."
        except ChatWriteForbidden:
            return "❌ Бот не может писать в этот канал. Дайте права на публикацию."
        except UsernameNotOccupied:
            return "❌ Канал с таким username не существует."
        except Exception as e:
            logger.exception(f"Ошибка при получении информации о канале: {e}")
            return "⚠️ Произошла ошибка при проверке канала. Попробуйте позже."


        # Проверка, не добавлен ли уже этот канал
        existing_channel = await get_channel_by_id(chat.id, session)
        if existing_channel:
            return f"⚠️ Канал {chat.id} уже добавлен другим пользователем."

        # Добавление канала
        channel_data = {
            "channel_id": chat.id,
            "username": chat.username,
            "description": chat.description,
            "type_channel": chat.type,
            "is_private_channel": chat.username is None,
            "start_count_subs": chat.members_count if hasattr(chat, "members_count") else None,
            "join_at": datetime.utcnow(),
        }

        await create_channel(channel_data, session)
        await update_user_channel_id(user_id, chat.id, session)

        waiting_channel.pop(user_id, None)
        logger.info(f"✅ Канал {chat.id} добавлен пользователем {user_id}")
        return f"✅ Канал {chat.id} успешно добавлен!"
