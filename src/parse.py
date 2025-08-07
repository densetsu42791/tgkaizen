# # src/parse.py
# from pyrogram import Client
# from pyrogram.enums import ChatType
# from pyrogram.errors import FloodWait
# from pyrogram.raw.functions.channels import GetParticipants
# from pyrogram.raw.types import (
#     ChannelParticipantsAdmins, ChannelParticipantsBanned, ChannelParticipantsBots,
#     ChannelParticipantsContacts, ChannelParticipantsKicked, ChannelParticipantsMentions,
#     ChannelParticipantsRecent, ChannelParticipantsSearch
# )
# from utils.logger import logger
# from db.crud import add_subscriber
# from db.async_session import async_session
# import asyncio
# from string import ascii_lowercase, digits


# # Основной алфавит + английские буквы + цифры
# LETTERS = list("абвгдеёжзийклмнопрстуфхцчшщьыэюя") + list(ascii_lowercase) + list(digits)

# # Дополнительные символы, которые могут быть в именах или юзернеймах
# EXTRA_SYMBOLS = list("_-. ")
# LETTERS += EXTRA_SYMBOLS

# FILTERS = [
#     ChannelParticipantsAdmins(),
#     ChannelParticipantsBanned(q=''),
#     ChannelParticipantsBots(),
#     ChannelParticipantsContacts(q=''),
#     ChannelParticipantsKicked(q=''),
#     ChannelParticipantsMentions(q=''),
#     ChannelParticipantsRecent(),
# ]

# userbot_client: Client = None

# def set_userbot_client(client: Client):
#     global userbot_client
#     userbot_client = client


# # async def _fetch_users(channel_peer, filter_obj, seen_ids: set, channel_chat, collected: list) -> None:
# #     offset, limit = 0, 100
# #     while True:
# #         result = await userbot_client.invoke(
# #             GetParticipants(channel=channel_peer, filter=filter_obj, offset=offset, limit=limit, hash=0)
# #         )

# #         if not result.users:
# #             break

# #         async with async_session() as session:
# #             for raw_user in result.users:
# #                 if raw_user.id in seen_ids:
# #                     continue
# #                 seen_ids.add(raw_user.id)

# #                 try:
# #                     # Получаем полноценного пользователя через get_users
# #                     user = await userbot_client.get_users(raw_user.id)

# #                     class FakeChatMemberUpdated:
# #                         new_chat_member = None
# #                         invite_link = getattr(raw_user, 'invite_link', None)

# #                     subscriber = await add_subscriber(
# #                         session=session,
# #                         user=user,
# #                         chat=channel_chat,
# #                         chat_member_updated=FakeChatMemberUpdated()
# #                     )
# #                     collected.append(subscriber)

# #                 except Exception as e:
# #                     logger.error(f"Ошибка при добавлении пользователя {raw_user.id}: {e}")


# #         offset += len(result.users)
# #         logger.info(f"→ {filter_obj.__class__.__name__}: получено {len(result.users)} | всего: {len(collected)}")

# #         if len(result.users) < limit:
# #             break
# #         await asyncio.sleep(30)


# async def _fetch_users(channel_peer, filter_obj, seen_ids: set, channel_chat, collected: list) -> None:
#     offset, limit = 0, 100
#     while True:
#         try:
#             result = await userbot_client.invoke(
#                 GetParticipants(channel=channel_peer, filter=filter_obj, offset=offset, limit=limit, hash=0)
#             )
            
#             if not result.users:
#                 break
                
#             async with async_session() as session:
#                 for raw_user in result.users:
#                     if raw_user.id in seen_ids:
#                         continue
#                     seen_ids.add(raw_user.id)
                    
#                     try:
#                         user = await userbot_client.get_users(raw_user.id)
                        
#                         class FakeChatMemberUpdated:
#                             new_chat_member = None
#                             invite_link = getattr(raw_user, 'invite_link', None)
                            
#                         subscriber = await add_subscriber(session=session, user=user, chat=channel_chat, chat_member_updated=FakeChatMemberUpdated())
#                         collected.append(subscriber)
#                     except Exception as e:
#                         logger.error(f"Ошибка при добавлении пользователя {raw_user.id}: {e}")
    
#             offset += len(result.users)
#             logger.info(f"→ {filter_obj.__class__.__name__}: получено {len(result.users)} | всего: {len(collected)}")
        
#             if len(result.users) < limit:
#                 delay = max((limit - len(result.users)) * 0.5, 1)
#             else:
#                 delay = 1
#             await asyncio.sleep(delay)
#         except FloodWait as e:
#             logger.warning(f"FloodWait detected! Waiting for {e.x} seconds...")
#             await asyncio.sleep(e.x)
#             continue
#         finally:
#             await asyncio.sleep(1)  # Небольшая пауза после каждого цикла


# async def parsing_with_userbot(channel_id: int) -> int:
#     if userbot_client is None:
#         raise RuntimeError("userbot_client не установлен.")

#     logger.info(f"Начинаем парсинг канала {channel_id}")
#     chat = await userbot_client.get_chat(channel_id)
#     if chat.type not in (ChatType.CHANNEL, ChatType.SUPERGROUP):
#         return "Это не канал или супергруппа."

#     peer = await userbot_client.resolve_peer(channel_id)
#     collected_subs, seen_ids = [], set()

#     # Проход по основным фильтрам
#     for f in FILTERS:
#         await _fetch_users(peer, f, seen_ids, chat, collected_subs)

#     # Поиск по всем символам
#     for symbol in LETTERS:
#         before = len(collected_subs)
#         await _fetch_users(peer, ChannelParticipantsSearch(q=symbol), seen_ids, chat, collected_subs)
#         added = len(collected_subs) - before
#         logger.info(f"Символ '{symbol}' добавил {added} новых подписчиков")

#     # Пустой поиск как дополнительная попытка
#     logger.info("Выполняем пустой ChannelParticipantsSearch для добора")
#     before = len(collected_subs)
#     await _fetch_users(peer, ChannelParticipantsSearch(q=''), seen_ids, chat, collected_subs)
#     logger.info(f"Пустой поиск добавил {len(collected_subs) - before} новых подписчиков")

#     logger.info(f"Всего собрано {len(collected_subs)} уникальных подписчиков.")
#     return len(collected_subs)


import asyncio
from string import ascii_lowercase, digits
from typing import Optional

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.raw.functions.channels import GetParticipants
from pyrogram.raw.types import (
    ChannelParticipantsAdmins, ChannelParticipantsBanned, ChannelParticipantsBots,
    ChannelParticipantsContacts, ChannelParticipantsKicked, ChannelParticipantsMentions,
    ChannelParticipantsRecent, ChannelParticipantsSearch
)

from utils.logger import logger
from db.crud import add_subscriber
from db.async_session import async_session

# Символы для поиска пользователей по ChannelParticipantsSearch
LETTERS: list[str] = list("абвгдеёжзийклмнопрстуфхцчшщьыэюя") + list(ascii_lowercase) + list(digits)
LETTERS += list("_-. ")

# Набор фильтров для получения подписчиков
FILTERS = [
    ChannelParticipantsAdmins(),
    ChannelParticipantsBanned(q=''),
    ChannelParticipantsBots(),
    ChannelParticipantsContacts(q=''),
    ChannelParticipantsKicked(q=''),
    ChannelParticipantsMentions(q=''),
    ChannelParticipantsRecent(),
]

# Глобальная переменная клиента
userbot_client: Optional[Client] = None


def set_userbot_client(client: Client) -> None:
    """
    Устанавливает клиент userbot, который используется для парсинга.
    """
    global userbot_client
    userbot_client = client


async def _fetch_users(
    channel_peer,
    filter_obj,
    seen_ids: set[int],
    channel_chat,
    collected: list
) -> None:
    """
    Получает пользователей по заданному фильтру и добавляет в базу данных.

    :param channel_peer: объект канала
    :param filter_obj: фильтр участников
    :param seen_ids: множество уже обработанных ID
    :param channel_chat: объект чата Pyrogram
    :param collected: список для хранения добавленных пользователей
    """
    offset, limit = 0, 100

    while True:
        try:
            result = await userbot_client.invoke(
                GetParticipants(
                    channel=channel_peer,
                    filter=filter_obj,
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )

            if not result.users:
                break

            async with async_session() as session:
                for raw_user in result.users:
                    if raw_user.id in seen_ids:
                        continue

                    seen_ids.add(raw_user.id)

                    try:
                        user = await userbot_client.get_users(raw_user.id)

                        class FakeChatMemberUpdated:
                            new_chat_member = None
                            invite_link = getattr(raw_user, 'invite_link', None)

                        subscriber = await add_subscriber(
                            session=session,
                            user=user,
                            chat=channel_chat,
                            chat_member_updated=FakeChatMemberUpdated()
                        )
                        collected.append(subscriber)

                    except Exception as e:
                        logger.error(f"Ошибка при добавлении пользователя {raw_user.id}: {e}")

            offset += len(result.users)
            logger.info(
                f"→ {filter_obj.__class__.__name__}: получено {len(result.users)} | всего: {len(collected)}"
            )

            delay = max((limit - len(result.users)) * 0.5, 1) if len(result.users) < limit else 1
            await asyncio.sleep(delay)

        except FloodWait as e:
            logger.warning(f"FloodWait: ожидание {e.x} секунд...")
            await asyncio.sleep(e.x)
            continue

        finally:
            await asyncio.sleep(1)  # Защита от флуда


async def parsing_with_userbot(channel_id: int) -> int:
    """
    Запускает парсинг канала с использованием userbot.

    :param channel_id: ID или username канала
    :return: Количество уникальных подписчиков
    """
    if userbot_client is None:
        raise RuntimeError("userbot_client не установлен. Используй set_userbot_client() перед вызовом.")

    logger.info(f"Запуск парсинга канала {channel_id}")
    chat = await userbot_client.get_chat(channel_id)

    if chat.type not in (ChatType.CHANNEL, ChatType.SUPERGROUP):
        raise ValueError("Указанный объект не является каналом или супергруппой.")

    peer = await userbot_client.resolve_peer(channel_id)
    collected_subs: list = []
    seen_ids: set[int] = set()

    # Сначала проходим по предопределённым фильтрам
    for filter_obj in FILTERS:
        await _fetch_users(peer, filter_obj, seen_ids, chat, collected_subs)

    # Поиск по всем символам из LETTERS
    for symbol in LETTERS:
        before = len(collected_subs)
        await _fetch_users(peer, ChannelParticipantsSearch(q=symbol), seen_ids, chat, collected_subs)
        added = len(collected_subs) - before
        logger.info(f"Символ '{symbol}' → добавлено {added} подписчиков")

    # Дополнительная попытка пустым поиском
    logger.info("Пробуем пустой ChannelParticipantsSearch...")
    before = len(collected_subs)
    await _fetch_users(peer, ChannelParticipantsSearch(q=''), seen_ids, chat, collected_subs)
    logger.info(f"Пустой поиск → добавлено {len(collected_subs) - before} подписчиков")

    logger.info(f"Завершено. Собрано {len(collected_subs)} уникальных подписчиков.")
    return len(collected_subs)
