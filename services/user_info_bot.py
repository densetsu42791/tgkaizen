from pyrogram import Client
from pyrogram.types import User

async def get_info_user_with_bot(client: Client, user_id: int) -> str:
    user: User = await client.get_users(user_id)

    info = [
        f"👤 ID: {user.id}",
        f"🙋‍♂️ Имя: {user.first_name}",
        f"👨‍💼 Фамилия: {user.last_name or '—'}",
        f"💬 Username: @{user.username}" if user.username else "💬 Username: —",
        f"🌐 Язык: {user.language_code or 'неизвестен'}",
        f"🤖 Бот: {'Да' if user.is_bot else 'Нет'}",
        f"🤖 Phone: {user.phone_number}"

    ]

    return "\n".join(info)
