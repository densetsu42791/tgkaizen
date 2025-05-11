from pyrogram import Client
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant, ChannelInvalid, PeerIdInvalid, RPCError
from app.db.session import async_session
from app.db.models import User, Channel
from sqlalchemy import select
import logging
from app.utils.user_state import waiting_channel

logger = logging.getLogger(__name__)


async def process_channel_addition(client: Client, user_id: int, command_call=False, message: Message = None) -> str:
    async with async_session() as session:

        # Проверка: есть ли Юзер в базе
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return "Сначала нажмите /start"

        if command_call:
            waiting_channel[user_id] = True
            return "Перешлите сообщение из канала."

        # Попытка извлечь ID канала из пересланного сообщения
        try:
            chat = message.forward_from_chat
            logger.info(f"CHAT: {chat}")
            if not chat:
                raise ValueError("Нет пересланного чата")

            full_chat = await client.get_chat(chat.id)

        except Exception as e:
            logger.warning(f"Ошибка при получении канала: {e}")
            return "❌ Ошибка при получении канала."

        # Проверка: Канал уже добавлен?
        result = await session.execute(select(Channel).where(Channel.channel_id == full_chat.id))
        already_linked = result.scalar_one_or_none()

        if already_linked:
            return f"Канал {full_chat.title} уже добавлен."

        # Создание канала
        new_channel = Channel(
            channel_id=full_chat.id,
            title=full_chat.title,
            user_id=user_id
        )
        session.add(new_channel)
        await session.commit()


        waiting_channel.pop(user_id, None)


        return full_chat.title
