# plgs/parse_subs.py
# from pyrogram import Client, filters
# from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from src.parse import parsing_with_userbot
# from utils.logger import logger


# @Client.on_callback_query(filters.regex(r"^parsing:[\w\-]+$"))
# async def cb_parsing(client: Client, callback: CallbackQuery):
#     user_id = callback.from_user.id
#     channel_id = int(callback.data.split(":")[1])

#     logger.info(f"Пользователь {user_id} вызвал парсинг канала {channel_id}")
#     await callback.answer("Запускаем парсинг...")

#     try:
#         result = await parsing_with_userbot(channel_id)

#     except Exception as e:
#         logger.exception("Ошибка при получении информации о пользователе:")
#         await callback.message.edit_text("Произошла ошибка при обработке запроса.")

#     await callback.message.reply(
#             f"✅ Собрано и сохранено {result} уникальных подписчиков.",
#             reply_markup=InlineKeyboardMarkup([
#                 [InlineKeyboardButton("Перейти к каналу", callback_data=f"get_info_channel:{channel_id}")],
#                 [InlineKeyboardButton("Главное меню", callback_data="start")]
#             ])
#         )



# plgs/parse_subs.py
# from pyrogram import Client, filters
# from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from src.parse import parsing_with_userbot
# from utils.logger import logger
# import asyncio
# from pyrogram.errors import FloodWait

# @Client.on_callback_query(filters.regex(r"^parsing:[\w\-]+$"))
# async def cb_parsing(client: Client, callback: CallbackQuery):
#     user_id = callback.from_user.id
#     channel_id = int(callback.data.split(":")[1])

#     logger.info(f"Пользователь {user_id} вызвал парсинг канала {channel_id}")
#     await callback.answer("Запускаем парсинг...")

#     try:
#         result = await parsing_with_userbot(channel_id)

#     # except FloodWait as e:
#     #     wait_time = e.value
#     #     logger.warning(f"FloodWait: нужно подождать {wait_time} секунд")
#     #     await callback.message.edit_text(f"⚠️ Telegram просит подождать {wait_time} секунд. Повторите позже.")
#     #     return

#     except Exception as e:
#         logger.exception("Ошибка при получении информации о пользователе:")
#         await callback.message.edit_text("❌ Произошла ошибка при обработке запроса.")
#         return

#     # сюда мы попадаем только если result успешно получен
#     await callback.message.reply(
#         f"✅ Собрано и сохранено {result} уникальных подписчиков.",
#         reply_markup=InlineKeyboardMarkup([
#             [InlineKeyboardButton("Перейти к каналу", callback_data=f"get_info_channel:{channel_id}")],
#             [InlineKeyboardButton("Главное меню", callback_data="start")]
#         ])
#     )


import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from src.parse import parsing_with_userbot
from utils.logger import logger


@Client.on_callback_query(filters.regex(r"^parsing:\d+$"))
async def cb_parsing(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик кнопки парсинга подписчиков канала.

    :param client: экземпляр клиента Pyrogram
    :param callback: объект CallbackQuery от пользователя
    """
    user_id = callback.from_user.id
    channel_id_str = callback.data.split(":")[1]

    try:
        channel_id = int(channel_id_str)
    except ValueError:
        logger.warning(f"Некорректный channel_id от пользователя {user_id}: {channel_id_str}")
        await callback.answer("Некорректный ID канала.")
        return

    logger.info(f"Пользователь {user_id} инициировал парсинг канала {channel_id}")
    await callback.answer("⏳ Запускаем парсинг...")

    try:
        result = await parsing_with_userbot(channel_id)

    except FloodWait as e:
        logger.warning(f"FloodWait: ожидание {e.x} секунд при парсинге канала {channel_id}")
        await callback.message.edit_text(
            f"⚠️ Telegram просит подождать {e.x} секунд. Повторите позже."
        )
        return

    except Exception as e:
        logger.exception(f"Ошибка при парсинге канала {channel_id}: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при парсинге. Попробуйте позже.")
        return

    # Успешно завершён парсинг
    await callback.message.reply(
        f"✅ Собрано и сохранено {result} уникальных подписчиков.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Инфо о канале", callback_data=f"get_info_channel:{channel_id}")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ])
    )




############
# import asyncio

# from pyrogram import Client, filters
# from pyrogram.errors import FloodWait
# from pyrogram.types import (
#     CallbackQuery,
#     InlineKeyboardButton,
#     InlineKeyboardMarkup
# )

# from src.parse import parsing_with_userbot
# from utils.logger import logger


# @Client.on_callback_query(filters.regex(r"^parsing:\d+$"))
# async def cb_parsing(client: Client, callback: CallbackQuery) -> None:
#     """
#     Обработчик кнопки парсинга подписчиков канала.

#     :param client: экземпляр клиента Pyrogram
#     :param callback: объект CallbackQuery от пользователя
#     """
#     user_id = callback.from_user.id
#     channel_id_str = callback.data.split(":")[1]

#     try:
#         channel_id = int(channel_id_str)
#     except ValueError:
#         logger.warning(f"Некорректный channel_id от пользователя {user_id}: {channel_id_str}")
#         await callback.answer("Некорректный ID канала.")
#         return

#     logger.info(f"Пользователь {user_id} инициировал парсинг канала {channel_id}")
#     await callback.answer("⏳ Запускаем парсинг...")

#     try:
#         result = await parsing_with_userbot(channel_id)

#     except FloodWait as e:
#         logger.warning(f"FloodWait: ожидание {e.x} секунд при парсинге канала {channel_id}")
#         await callback.message.edit_text(
#             f"⚠️ Telegram просит подождать {e.x} секунд. Повторите позже."
#         )
#         return

#     except Exception as e:
#         logger.exception(f"Ошибка при парсинге канала {channel_id}: {e}")
#         await callback.message.edit_text("❌ Произошла ошибка при парсинге. Попробуйте позже.")
#         return

#     # Успешно завершён парсинг
#     await callback.message.reply(
#         f"✅ Собрано и сохранено {result} уникальных подписчиков.",
#         reply_markup=InlineKeyboardMarkup([
#             [InlineKeyboardButton("📊 Инфо о канале", callback_data=f"get_info_channel:{channel_id}")],
#             [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
#         ])
#     )



# plgs/parse_subs.py
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from src.parse import parsing_with_userbot
from utils.logger import logger


# @Client.on_callback_query(filters.regex(r"^parsing:\d+$"))
@Client.on_callback_query(filters.regex(r"^parsing:[\w\-]+$"))
async def cb_parsing(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик кнопки парсинга подписчиков канала.

    :param client: экземпляр клиента Pyrogram
    :param callback: объект CallbackQuery от пользователя
    """
    logger.info(f"Нажата кнопка Парсинг")
    user_id = callback.from_user.id
    channel_id_str = callback.data.split(":")[1]

    try:
        channel_id = int(channel_id_str)
    except ValueError:
        logger.warning(f"Некорректный channel_id от пользователя {user_id}: {channel_id_str}")
        await callback.answer("Некорректный ID канала.")
        return

    logger.info(f"Пользователь {user_id} инициировал парсинг канала {channel_id}")
    await callback.answer("⏳ Запускаем парсинг...")

    try:
        result = await parsing_with_userbot(channel_id)

    except FloodWait as e:
        logger.warning(f"FloodWait: ожидание {e.x} секунд при парсинге канала {channel_id}")
        await callback.message.edit_text(
            f"⚠️ Telegram просит подождать {e.x} секунд. Повторите позже."
        )
        return

    except Exception as e:
        logger.exception(f"Ошибка при парсинге канала {channel_id}: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при парсинге. Попробуйте позже.")
        return

    # Успешно завершён парсинг
    await callback.message.reply(
        f"✅ Собрано и сохранено {result} уникальных подписчиков.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Инфо о канале", callback_data=f"get_info_channel:{channel_id}")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ])
    )
