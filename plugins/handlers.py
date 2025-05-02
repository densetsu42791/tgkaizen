from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.database import check_user, add_channel
from pyrogram.types import CallbackQuery
from pyrogram.enums import ChatType
import logging


logger = logging.getLogger(__name__)

waiting_channel_input = {}


@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f"User {user_id} started the bot.")
    
    channel_id = await check_user(user_id, username, first_name, last_name)
    
    if channel_id:
        button_text = channel_id
    else:
        button_text = "Добавить канал"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_text, callback_data="add_channel")],
        [InlineKeyboardButton("Admin", callback_data="admin")]
    ])

    await message.reply_text(f"Hi {first_name}!", reply_markup=keyboard)


@Client.on_callback_query(filters.regex("add_channel"))
async def add_channel_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    waiting_channel_input[user_id] = True  # устанавливаем флаг ожидания канала
    await callback_query.message.reply_text(
        "🔗 Пожалуйста, добавьте бота в ваш канал с правами администратора и пришлите его username.\n\n"
        "Пример: `@mychannelname` или `https://t.me/mychannelname`",
        quote=True
    )
    await callback_query.answer()




@Client.on_message(filters.text & filters.private)
async def receive_channel_username(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in waiting_channel_input:
        return

    input_username = message.text
    chat = await client.get_chat(input_username)

    # try:
    channel_username = await add_channel(client, user_id, chat)
    # except ValueError as e:
    #     await message.reply(f"❌ {str(e)}")
    #     return


    waiting_channel_input.pop(user_id) # Удаляем ожидание

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{channel_username}", callback_data="noop")],
        [InlineKeyboardButton("Admin", callback_data="admin")]
    ])
    await message.reply(f"✅ Канал успешно добавлен!", reply_markup=keyboard)








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


        


