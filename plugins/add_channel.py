from pyrogram import Client, filters
from pyrogram.types import Message
from src.channels import process_channel_addition
from src.user_state import waiting_channel


import logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("add_channel") & filters.private)
async def cmd_add_channel(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} вызвал \add_channel.")
    response = await process_channel_addition(client, user_id, command_call=True)
    await message.reply_text(response)


@Client.on_message(filters.private & filters.forwarded)
async def receive_forwarded_channel_message(client: Client, message: Message):
    user_id = message.from_user.id
    if waiting_channel.get(user_id):
        response = await process_channel_addition(client, user_id, message=message)
        logger.info(f"User {user_id} отправил сообщение.")
        await message.reply_text(response)





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

