from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.database import check_user
import logging


logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f"User {user_id} started the bot.")
    
    await check_user(user_id)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Admin", callback_data="admin")]
    ])

    await message.reply_text(f"Hi: {user_id}!", 
                             reply_markup=keyboard)




# @Client.on_message(filters.command("start"))
# async def start_command(client, message: Message):
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name

#     logger.info(f"User {user_id} started the bot. Username: {username}")

#     await ensure_user_exists(user_id, username, first_name)

#     channel = await is_channel_linked(user_id)
#     if channel:
#         button_text = channel
#     else:
#         button_text = "Добавить канал"

#     keyboard = InlineKeyboardMarkup([
#         [InlineKeyboardButton(button_text, callback_data="add_channel")],
#         [InlineKeyboardButton("Admin", callback_data="admin")]
#     ])
#     await message.reply_text(f"Hi {username}!", reply_markup=keyboard)




#################################################################


# @Client.on_callback_query()
# async def button_click(client, callback_query):
#     data = callback_query.data
#     if data == "add_channel":
#         await callback_query.edit_message_text("Добавим канал?", reply_markup=keyboard)
#     elif data == "admin":
#         await callback_query.edit_message_text("Это для админа", reply_markup=keyboard)


# @Client.on_callback_query()
# async def button_click(client, callback_query):
#     data = callback_query.data
#     if data == "count_members":
#         members_count = await client.get_chat_members_count(CHANNEL_NAME)
#         timestamp = datetime.now().strftime("%H:%M:%S")  # Временная отметка
#         new_text = f"В канале {CHANNEL_NAME} сейчас {members_count} подписчиков ({timestamp})."
#         await callback_query.edit_message_text(new_text, reply_markup=keyboard)
#     elif data == "help":
#         await callback_query.edit_message_text("Это страница помощи.", reply_markup=keyboard)


        


