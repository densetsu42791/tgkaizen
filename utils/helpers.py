from pyrogram import Client
from pyrogram.enums import ChatType


async def validate_forwarded_channel(client: Client, chat):
    if not chat:
        return "❌ Не удалось распознать канал."

    if chat.type != ChatType.CHANNEL:
        return "❌ Это не канал. Перешлите сообщение из канала."

    member = await client.get_chat_member(chat.id, client.me.id)
    privileges = getattr(member, "privileges", None)
    if privileges is None or not privileges.can_post_messages:
        return "❌ У бота нет прав администратора. Назначьте его админом канала."

    return None