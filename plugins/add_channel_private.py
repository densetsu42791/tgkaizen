from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message, Chat
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, UsernameInvalid, UsernameNotOccupied
from db.crud import add_channel_to_user
from services.user_state import user_waiting_input
from services.channel_service import (check_is_channel, check_bot_in_channel, parse_channel_username)
from utils.exceptions import NotAChannelError, BotNotAdminError

import logging
logger = logging.getLogger(__name__)
logger.info("Файл add_channel.py загружен")


waiting_private_channel = {}


@Client.on_message(filters.command("add_channel_private") & filters.private)
async def cmd_add_private_channel(client: Client, message: Message):
    logger.info("Команда /add_channel_private получена")
    user_id = message.from_user.id

    await message.reply_text(
        "🔒 Добавьте бота в свой **приватный канал** с правами администратора, "
        "а затем **перешлите любое сообщение из этого канала** сюда.",
        reply_markup=cancel_button()
    )
    waiting_private_channel[user_id] = True





@Client.on_message(filters.private & filters.forwarded)
async def receive_forwarded_channel_message(client: Client, message: Message):
    user_id = message.from_user.id
    if not waiting_private_channel.get(user_id):
        return

    if not message.forward_from_chat:
        await message.reply_text(
            "❌ Не удалось определить канал. Убедитесь, что вы переслали сообщение из канала.",
            reply_markup=cancel_button()
        )
        return

    chat = message.forward_from_chat

    try:
        if chat.type != ChatType.CHANNEL:
            raise NotAChannelError("Это не канал")

        await check_bot_in_channel(client, chat)

        await add_channel_to_user(client, user_id, chat)

        channel_username = chat.username or f"(ID: {chat.id})"

        await message.reply_text(f"✅ Приватный канал {channel_username} успешно подключён!")
        waiting_private_channel[user_id] = False

    except NotAChannelError:
        await message.reply_text(
            "❌ Это не канал. Пожалуйста, пересылайте сообщение именно из канала.",
            reply_markup=cancel_button()
        )
        waiting_private_channel[user_id] = True

    except BotNotAdminError:
        await message.reply_text(
            "❌ Бот не добавлен в канал или не имеет прав администратора.",
            reply_markup=cancel_button()
        )
        waiting_private_channel[user_id] = True

    except Exception as e:
        logger.exception("Ошибка при добавлении приватного канала")
        await message.reply_text(
            f"⚠️ Произошла ошибка: {e}\nПопробуйте ещё раз.",
            reply_markup=cancel_button()
        )
        waiting_private_channel[user_id] = True


@Client.on_callback_query(filters.regex("^cancel_input$"))
async def cancel_any_input(client: Client, callback_query):
    user_id = callback_query.from_user.id
    user_waiting_input[user_id] = False
    waiting_private_channel[user_id] = False
    await callback_query.message.edit_text("❌ Отменено. Вы можете начать заново.")



def cancel_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_input")]
    ])



# @Client.on_message(filters.command("add_channel") & filters.private)
# async def cmd_add_channel(client: Client, message: Message):
#     user_id = message.from_user.id

#     await message.reply_text(
#         "🔗 Добавьте бота в свой канал с правами администратора и затем отправьте адрес канала в сообщении ниже.\n\n"
#         "Пример: `@mychannelname` или `https://t.me/mychannelname`"
#     )
#     user_waiting_input[user_id] = True


# @Client.on_message(filters.private & filters.text & ~filters.command(["start"]))
# async def receive_channel_username(client: Client, message: Message):
#     user_id = message.from_user.id
#     if not user_waiting_input.get(user_id):
#         return

#     input_text = message.text.strip()
#     try:
#         username = parse_channel_username(input_text)
#         chat: Chat = await client.get_chat(username)

#         check_is_channel(chat)
#         await check_bot_in_channel(client, chat)

#         await add_channel_to_user(client, user_id, chat)

#         await message.reply_text(f"✅ Канал @{chat.username or 'Private'} успешно подключён!")
#         user_waiting_input[user_id] = False

#     except (PeerIdInvalid, UsernameInvalid, UsernameNotOccupied):
#         await message.reply_text(
#             "❌ Канал с таким адресом не найден.\nПожалуйста, исправьте и попробуйте ещё раз.",
#             reply_markup=cancel_button()
#         )
#         user_waiting_input[user_id] = True

#     except NotAChannelError:
#         await message.reply_text(
#             "❌ Это не канал. Пожалуйста, отправьте ссылку на канал и попробуйте ещё раз.",
#             reply_markup=cancel_button()
#         )
#         user_waiting_input[user_id] = True

#     except BotNotAdminError:
#         await message.reply_text(
#             "❌ Бот не добавлен в канал или не имеет прав администратора.\nПроверьте это и попробуйте ещё раз.",
#             reply_markup=cancel_button()
#         )
#         user_waiting_input[user_id] = True

#     except Exception as e:
#         logger.exception("Ошибка при добавлении канала")
#         await message.reply_text(
#             f"⚠️ Произошла ошибка: {e}\nПопробуйте ещё раз.",
#             reply_markup=cancel_button()
#         )
#         user_waiting_input[user_id] = True


# @Client.on_callback_query(filters.regex("^cancel_input$"))
# async def cancel_channel_input(client: Client, callback_query):
#     user_id = callback_query.from_user.id
#     user_waiting_input[user_id] = False
#     await callback_query.message.edit_text("❌ Отменено. Вы можете начать заново.")

# def cancel_button():
#     return InlineKeyboardMarkup([
#         [InlineKeyboardButton("❌ Отмена", callback_data="cancel_input")]
#     ])


