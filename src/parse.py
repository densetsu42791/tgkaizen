from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.raw.functions.channels import GetParticipants
from pyrogram.raw.types import (
    ChannelParticipantsAdmins, ChannelParticipantsBanned, ChannelParticipantsBots,
    ChannelParticipantsContacts, ChannelParticipantsKicked, ChannelParticipantsMentions,
    ChannelParticipantsRecent, ChannelParticipantsSearch
)
from utils.logger import logger
from db.crud import add_many_subscribers
from db.async_session import async_session
import asyncio


LETTERS = list("абвгдеёжзийклмнопрстуфхцчшщьыэюяabcdefghijklmnopqrstuvwxyz0123456789")
FILTERS = [
    ChannelParticipantsAdmins(),
    ChannelParticipantsBanned(q=''),
    ChannelParticipantsBots(),
    ChannelParticipantsContacts(q=''),
    ChannelParticipantsKicked(q=''),
    ChannelParticipantsMentions(q=''),
    ChannelParticipantsRecent(),
]


userbot_client: Client = None

def set_userbot_client(client: Client):
    global userbot_client
    userbot_client = client


async def _fetch_users(channel_peer, filter_obj, seen_ids: set, collected: list) -> None:
    offset, limit = 0, 100
    while True:
        result = await userbot_client.invoke(
            GetParticipants(channel=channel_peer, filter=filter_obj, offset=offset, limit=limit, hash=0)
        )

        if not result.users:
            break

        for user in result.users:
            if user.id not in seen_ids:
                seen_ids.add(user.id)
                collected.append({
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "invite_link": getattr(user, 'invite_link', None),
                    "phone_number": getattr(user, "phone", None),
                    "channel_id": int(f"-100{channel_peer.channel_id}"),
                })

        offset += len(result.users)
        logger.info(f"→ {filter_obj.__class__.__name__}: получено {len(result.users)} | всего: {len(collected)}")

        if len(result.users) < limit:
            break
        await asyncio.sleep(10)


async def parsing_with_userbot(channel_id: int) -> int:
    if userbot_client is None:
        raise RuntimeError("userbot_client не установлен.")

    logger.info(f"Начинаем парсинг канала {channel_id}")
    chat = await userbot_client.get_chat(channel_id)
    if chat.type not in (ChatType.CHANNEL, ChatType.SUPERGROUP):
        return "Это не канал или супергруппа."

    peer = await userbot_client.resolve_peer(channel_id)
    collected_subs, seen_ids = [], set()

    # Проход по основным фильтрам
    for f in FILTERS:
        await _fetch_users(peer, f, seen_ids, collected_subs)

    # Поиск по символам
    # for letter in LETTERS:
    #     await _fetch_users(peer, ChannelParticipantsSearch(q=letter), seen_ids, collected_subs)

    logger.info(f"Всего собрано {len(collected_subs)} уникальных подписчиков.")
    async with async_session() as session:
        await add_many_subscribers(subs_data=collected_subs, session=session)
    return len(collected_subs)





