# from pyrogram import Client

# async def get_info_user_with_userbot(client: Client, user_id: int) -> str:
#     user = await client.get_users(user_id)
    
#     if user.phone_number:
#         return f"📱 Телефон: +{user.phone_number}"
#     else:
#         return "📱 Телефон: не доступен (возможно, скрыт настройками приватности)"



from pyrogram import Client

# Глобальная переменная клиента (будет установлена из main.py)
userbot_client: Client = None

def set_userbot_client(client: Client):
    global userbot_client
    userbot_client = client

async def get_info_user_with_userbot(user_id: int) -> str:
    if userbot_client is None:
        raise RuntimeError("userbot_client не установлен. Вызови set_userbot_client(client) до использования.")

    user = await userbot_client.get_users(user_id)

    if user.phone_number:
        return f"📱 Телефон: +{user.phone_number}"
    else:
        return "📱 Телефон: не доступен (возможно, скрыт настройками приватности)"
