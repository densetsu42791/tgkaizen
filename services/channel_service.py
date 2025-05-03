from pyrogram import Client
from pyrogram.types import Chat
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant, ChannelPrivate

from utils.exceptions import NotAChannelError, BotNotAdminError


def parse_channel_username(input_text: str) -> str:
    """Парсит username из текста"""
    if input_text.startswith("https://t.me/"):
        return input_text.split("/")[-1]
    elif input_text.startswith("@"):
        return input_text[1:]
    return input_text


def check_is_channel(chat: Chat):
    """Проверяет, является ли чат каналом"""
    if chat.type != ChatType.CHANNEL:
        raise NotAChannelError("Это не канал")


async def check_bot_in_channel(client: Client, chat: Chat):
    """
    Проверяет, что бот добавлен в канал (публичный или приватный)
    и обладает правами администратора (если нужно).
    """
    try:
        member = await client.get_chat_member(chat.id, client.me.id)
    except UserNotParticipant:
        raise BotNotAdminError("Бот не добавлен в канал")
    except ChannelPrivate:
        raise BotNotAdminError("Канал приватный, и бот не имеет к нему доступа")

    privileges = getattr(member, "privileges", None)
    if privileges is None or not privileges.can_post_messages:
        raise BotNotAdminError("У бота нет прав администратора в канале")









# from pyrogram import Client
# from pyrogram.types import Chat
# from pyrogram.enums import ChatType
# from pyrogram.errors import UserNotParticipant
# from utils.exceptions import NotAChannelError, BotNotAdminError

# def parse_channel_username(input_text: str) -> str:
#     """Парсит username из текста"""
#     if input_text.startswith("https://t.me/"):
#         return input_text.split("/")[-1]
#     elif input_text.startswith("@"):
#         return input_text[1:]
#     return input_text


# def check_is_channel(chat: Chat):
#     """Проверяет, является ли чат каналом"""
#     if chat.type != ChatType.CHANNEL:
#         raise NotAChannelError("Это не канал")
    


# # Для публичного канала
# async def check_bot_in_channel(client: Client, chat: Chat):
#     """Проверяет, что бот добавлен в канал и имеет права администратора"""
#     try:
#         member = await client.get_chat_member(chat.id, client.me.id)
#     except UserNotParticipant:
#         raise BotNotAdminError("Бот не добавлен в канал")

#     privileges = getattr(member, "privileges", None)
#     if privileges is None or not privileges.can_post_messages:
#         raise BotNotAdminError("У бота нет прав администратора в канале")
