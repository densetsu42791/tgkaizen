# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from pyrogram.enums import ChatType
# from pyrogram.errors import ChannelPrivate, UserNotParticipant
# from db.crud import add_channel_to_user
# from services.user_state import user_waiting_input, waiting_private_channel
# from services.channel_service import check_bot_in_channel
# from utils.exceptions import NotAChannelError, BotNotAdminError

# import logging
# logger = logging.getLogger(__name__)


# @Client.on_message(filters.command("add_channel_private") & filters.private)
# async def cmd_add_channel_private(client: Client, message: Message):
#     user_id = message.from_user.id

#     await message.reply_text(
#         "🔒 Добавьте бота в свой **приватный канал** с правами администратора, "
#         "а затем **перешлите любое сообщение из этого канала** сюда."
#     )
#     waiting_private_channel[user_id] = True


# @Client.on_message(filters.private & filters.forwarded)
# async def receive_forwarded_channel_message(client: Client, message: Message):
#     user_id = message.from_user.id
#     if not waiting_private_channel.get(user_id):
#         return

#     if not message.forward_from_chat:
#         await message.reply_text(
#             "❌ Не удалось определить канал. Убедитесь, что вы переслали сообщение из канала.",
#             reply_markup=cancel_button()
#         )
#         return

#     chat = message.forward_from_chat

#     try:
#         if chat.type != ChatType.CHANNEL:
#             raise NotAChannelError("Это не канал.")
#         type_channel = 'channel'
#         is_private_channel = True
#         # Проверка доступа бота к каналу
#         await check_bot_in_channel(client, chat)
        

#         # Добавление канала
#         await add_channel_to_user(client, user_id, chat, type_channel, is_private_channel)

#         channel_username = chat.username or f"(ID: {chat.id})"
#         await message.reply_text(f"✅ Приватный канал {channel_username} успешно подключён!")

#         waiting_private_channel.pop(user_id, None)

#     except NotAChannelError:
#         await message.reply_text(
#             "❌ Это не канал. Пожалуйста, пересылайте сообщение именно из канала.",
#             reply_markup=cancel_button()
#         )
#     except BotNotAdminError:
#         await message.reply_text(
#             "❌ Бот не добавлен в канал или не имеет прав администратора.",
#             reply_markup=cancel_button()
#         )
#     except ChannelPrivate:
#         await message.reply_text(
#             "❌ Бот не может получить доступ к каналу. Возможно, он не добавлен.",
#             reply_markup=cancel_button()
#         )
#     except Exception as e:
#         logger.exception("Ошибка при добавлении приватного канала")
#         await message.reply_text(
#             f"⚠️ Произошла ошибка: {e}\nПопробуйте ещё раз.",
#             reply_markup=cancel_button()
#         )
#     finally:
#         waiting_private_channel[user_id] = True


# @Client.on_callback_query(filters.regex("^cancel_input$"))
# async def cancel_any_input(client: Client, callback_query):
#     user_id = callback_query.from_user.id
#     user_waiting_input[user_id] = False
#     waiting_private_channel[user_id] = False
#     await callback_query.message.edit_text("❌ Отменено. Вы можете начать заново.")


# def cancel_button():
#     return InlineKeyboardMarkup([
#         [InlineKeyboardButton("❌ Отмена", callback_data="cancel_input")]
#     ])

