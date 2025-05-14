# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from pyrogram.enums import ChatType

# from utils.user_context import set_state, get_state, clear_state
# from db.crud import add_channel, get_user_by_id, get_channel_by_id
# from db.session import async_session
# from utils.logger import logger

# from plgs.start import send_start_message  # Импортируем универсальную функцию


# @Client.on_callback_query(filters.regex(r"get_info_channel:{channel.channel_id}"))
# async def cb_test(client: Client, callback):
#     logger.info(f"Нажата кнопка: {callback.data}")
#     user_id = callback.from_user.id
    
#     logger.info(f"USER DD: {user_id}")

#     await callback.message.reply(f"{callback}")
#     await callback.answer()