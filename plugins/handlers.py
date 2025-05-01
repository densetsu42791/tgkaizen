from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.database import ensure_user_exists, is_channel_linked

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
    [InlineKeyboardButton("Admin", callback_data="admin")]
])

@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    await ensure_user_exists(user_id, username, first_name)
    channel_id = await is_channel_linked(user_id)

    await message.reply_text(f"Hi {username}!", reply_markup=START_BUTTONS)




#################################################################





# async def ensure_user_exists(user_id, username, first_name):
#     async with SessionLocal() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             now = datetime.now(timezone.utc)
#             if not user:
#                 session.add(User(
#                     user_id=user_id,
#                     username=username,
#                     first_name=first_name,
#                     join_at=now,
#                     last_vizit=now
#                 ))
#             else:
#                 user.last_vizit = now

# async def get_user_channel(user_id):
#     async with SessionLocal() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             if user and user.channel:
#                 return user.channel
#             return None

# @Client.on_message(filters.command("start"))
# async def start_command(client, message: Message):
#     print(f"/start вызван от {message.from_user.id}")  # отладка
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name

#     await ensure_user_exists(user_id, username, first_name)
#     channel = await get_user_channel(user_id)

#     if channel:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton(channel, callback_data="channel_info")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, вы уже подключили канал: {channel}", reply_markup=keyboard)
#     else:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, добро пожаловать в TgKaizen!\n\n⚠️ Канал не добавлен.", reply_markup=keyboard)




# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from db.database import SessionLocal
# from db.models import User
# from sqlalchemy.future import select
# from datetime import datetime, timezone


# async def ensure_user_exists(user_id, username, first_name):
#     async with SessionLocal() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             now = datetime.now(timezone.utc)
#             if not user:
#                 session.add(User(
#                     user_id=user_id,
#                     username=username,
#                     first_name=first_name,
#                     join_at=now,
#                     last_vizit=now
#                 ))
#             else:
#                 user.last_vizit = now

# async def get_user_channel(user_id):
#     async with SessionLocal() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             if user and user.linked_channel:
#                 return user.linked_channel.title
#             return None

# @Client.on_message(filters.command("start"))
# async def start_command(client, message: Message):
#     print(f"/start вызван от {message.from_user.id}")  # отладка
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name

#     await ensure_user_exists(user_id, username, first_name)
#     channel = await get_user_channel(user_id)

#     if channel:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton(channel, callback_data="channel_info")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, вы уже подключили канал: {channel}", reply_markup=keyboard)
#     else:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, добро пожаловать в TgKaizen!\n\n⚠️ Канал не добавлен.", reply_markup=keyboard)


# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from db.database import async_session
# from db.models import User, Channel
# from sqlalchemy.future import select
# from datetime import datetime, timezone


# async def ensure_user_exists(user_id, username, first_name):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             now = datetime.now(timezone.utc)
#             if not user:
#                 session.add(User(
#                     user_id=user_id,
#                     username=username,
#                     first_name=first_name,
#                     join_at=now,
#                     last_vizit=now
#                 ))
#             else:
#                 user.last_vizit = now

# async def get_user_channel(user_id):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             if user and user.linked_channel:
#                 return user.linked_channel.title
#             return None


# @Client.on_message(filters.command("start"))
# async def start_command(client: Client, message: Message):
#     print(f"Обработка /start от пользователя {message.from_user.id}")  # для отладки

#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name

#     await ensure_user_exists(user_id, username, first_name)
#     channel_title = await get_user_channel(user_id)

#     if channel_title:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton(channel_title, callback_data="channel_info")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, вы уже подключили канал: {channel_title}", reply_markup=keyboard)
#     else:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
#             [InlineKeyboardButton("Admin", callback_data="admin")]
#         ])
#         await message.reply_text(f"{first_name}, добро пожаловать в TgKaizen!\n\n⚠️ Канал не добавлен.", reply_markup=keyboard)



#############################################################

# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from db.database import async_session
# from db.models import User, Channel
# from sqlalchemy.future import select
# from datetime import datetime, timezone


# START_BUTTONS = InlineKeyboardMarkup([
#         [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
#         [InlineKeyboardButton("Admin", callback_data="admin")]
#     ])


# async def ensure_user_exists(user_id, username, first_name):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             if not user:
#                 session.add(User(
#                     user_id=user_id,
#                     username=username,
#                     first_name=first_name
#                 ))


# async def is_channel_linked(user_id):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(User).where(User.user_id == user_id))
#             user = result.scalars().first()
#             return user.channel if user else None


# @Client.on_message(filters.command("start"))
# async def start_command(client, message: Message):
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     await ensure_user_exists(user_id, username, first_name)
#     channel_id = await is_channel_linked(user_id)
#     if channel_id:
#         await message.reply_text(f"{first_name} добро пожаловать в TgKaizen!", reply_markup=START_BUTTONS)
#     else:
#         await message.reply_text(f"{first_name} добро пожаловать в TgKaizen!\n\n⚠️ Канал не добавлен.", reply_markup=START_BUTTONS)



###########################################################################

# from pyrogram import Client, filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from db.database import ensure_user_exists, is_channel_linked



# START_BUTTONS = InlineKeyboardMarkup([
#         [InlineKeyboardButton("Добавить канал", callback_data="add_channel")],
#         [InlineKeyboardButton("Admin", callback_data="admin")]
#     ])


# @Client.on_message(filters.command("start"))
# async def start_command(client, message: Message):
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name

#     await ensure_user_exists(user_id, username, first_name)

#     channel_id = await is_channel_linked(user_id)

#     #await message.reply_text("Добро пожаловать в TgKaizen!", reply_markup=START_BUTTONS)
#     if channel_id:
#         await message.reply_text(f"{first_name} добро пожаловать в TgKaizen!", reply_markup=START_BUTTONS)
#     else:
#         await message.reply_text(f"{first_name} добро пожаловать в TgKaizen!\n\n⚠️ Канал не добавлен.", reply_markup=START_BUTTONS)


############################################################################












# @Client.on_message(filters.command(["start"]))
# async def start_command(client, message):
#     await message.reply_text(
#         "Добро пожаловать в TgKaize!",
#         reply_markup=START_BUTTONS
#         )


# @Client.on_callback_query()
# async def button_click(client, callback_query):
#     data = callback_query.data
#     if data == "add_channel":
#         await callback_query.edit_message_text("Добавим канал?", reply_markup=keyboard)
#     elif data == "admin":
#         await callback_query.edit_message_text("Это для админа", reply_markup=keyboard)





##########################
# from pyrogram import Client, filters
# from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from datetime import datetime

# CHANNEL_NAME = "tgkaizen"  # Название канала, в котором считаем подписчиков

# keyboard = InlineKeyboardMarkup([
#         [InlineKeyboardButton("Сколько сейчас подписчиков?", callback_data="count_members")],
#         [InlineKeyboardButton("Помощь", callback_data="help")]
#     ])


# @Client.on_message(filters.command(['start']))
# async def start_command(client, message):
#     await message.reply_text(
#         "Добро пожаловать в наш бот!",
#         reply_markup=keyboard
#     )

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







# @Client.on_message(filters.command(['start', 'help']))
# async def command_handler(client, message):
#     if message.text == '/start':
#         await message.reply("Привет! Я ваш помощник-бот. Введите /help для получения списка команд.")
#     elif message.text == '/help':
#         await message.reply(
#             "Доступные команды:\n"
#             "/start - Приветственное сообщение\n"
#             "/help - Список команд")
        


