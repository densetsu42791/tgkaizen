from pyrogram import Client
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from db.async_session import async_session
from db.crud import (
    get_subscriber,
    add_subscriber,
    log_subscriber_event,
    update_left_at
)
import datetime
import traceback
from db.models import ActivityType


ADMIN_ID = 355527991


@Client.on_chat_member_updated()
async def handle_subscription_change(client: Client, chat_member_updated: ChatMemberUpdated):
    print("🔔 chat_member_updated triggered")
    try:
        old = chat_member_updated.old_chat_member
        new = chat_member_updated.new_chat_member
        user = chat_member_updated.from_user
        chat = chat_member_updated.chat

        if not user:
            print("❗ Нет информации о пользователе.")
            return

        user_id = user.id
        first_name = user.first_name or "Пользователь"
        channel_id = chat.id

        async with async_session() as session:
            # Подписка
            if new and new.status == ChatMemberStatus.MEMBER:
                subscriber = await get_subscriber(session, user_id, channel_id)
                if subscriber:
                    await client.send_message(chat_id=ADMIN_ID, text=f"Повторная подписка: {first_name}")
                else:
                    subscriber = await add_subscriber(session, user, chat, chat_member_updated)
                    await client.send_message(chat_id=ADMIN_ID, text=f"{first_name} подписался на канал {chat.title}")
                await log_subscriber_event(session, subscriber.id, ActivityType.SUBSCRIBED)

            # Отписка
            elif old and old.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR] and (not new or new.status == ChatMemberStatus.LEFT):
                await update_left_at(session, user_id, channel_id, left_at=datetime.datetime.utcnow())
                await client.send_message(chat_id=ADMIN_ID, text=f"{first_name} отписался от канала {chat.title}")
                subscriber = await get_subscriber(session, user_id, channel_id)
                if subscriber:
                    await log_subscriber_event(session, subscriber.id, ActivityType.UNSUBSCRIBED)
            else:
                print(f"⚠️ Необработанное изменение статуса: OLD={old.status if old else 'None'} → NEW={new.status if new else 'None'}")

    except Exception:
        print("❌ Ошибка при обработке chat_member_updated:")
        traceback.print_exc()