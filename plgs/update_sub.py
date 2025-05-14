from pyrogram import Client
from pyrogram.types import ChatMemberUpdated
from db.session import async_session
from db.crud import get_subscriber, add_subscriber, log_subscriber_event
from pyrogram.enums import ChatMemberStatus

@Client.on_chat_member_updated()
async def handle_subscription(client: Client, chat_member_updated: ChatMemberUpdated):
    print("✅ chat_member_updated triggered")

    new = chat_member_updated.new_chat_member
    user = chat_member_updated.from_user
    channel = chat_member_updated.chat

    print(f"NEW: {new}")
    print(f"USER: {user}")
    print(f"CHANNEL: {channel}")

    if not user or not new:
        print("❗ Недостаточно данных: user или new отсутствует")
        return
    print("✅ if not user or not new")
    user_id = user.id
    first_name = user.first_name
    channel_id = channel.id
    phone_number = user.phone_number

    if new.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR):
        print("✅ if new.status in ...")
        async with async_session() as session:
            
            subscriber = await get_subscriber(session, user_id, channel_id)
            print(f"✅ SUBSCRIBER: {subscriber}")
            if subscriber:
                await client.send_message(chat_id=user_id, text=f"🔁 Повторная подписка: {first_name}")
            else:
                await add_subscriber(session, user_id, first_name, invite_link=None, channel_id=channel_id, phone_number=phone_number)
                await client.send_message(chat_id=user_id, text=f"🆕 Новый подписчик: {first_name}")
            await log_subscriber_event(session, user_id, channel_id, event_type="SUBSCRIBED")




@Client.on_chat_member_updated()
async def handle_unsubscription(client: Client, chat_member_updated: ChatMemberUpdated):
    print("🚫 chat_member_updated (unsub) triggered")

    new = chat_member_updated.new_chat_member
    user = chat_member_updated.from_user
    channel = chat_member_updated.chat

    if not user or not new:
        print("❗ Недостаточно данных: user или new отсутствует")
        return

    user_id = user.id
    first_name = user.first_name or "Пользователь"
    channel_id = channel.id

    if new.status in ("left", "kicked"):
        async with async_session() as session:
            await log_subscriber_event(session, user_id, channel_id, event_type="left")
            await client.send_message(channel_id, f"📤 Отписка: {first_name}")
