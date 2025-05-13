from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.crud import get_user_by_id, create_user, get_user_channels
from app.db.session import async_session
from app.logger import logger
from app.utils.user_context import set_state


async def send_start_message(client: Client, user_id: int):
    async with async_session() as session:
        db_user = await get_user_by_id(session, user_id)
        if not db_user:
            return

        channels = await get_user_channels(session, user_id)
        text = f"Hi, {db_user.first_name}"
        buttons = [
            [InlineKeyboardButton(text=channel.title, callback_data=f"get_info_channel:{channel.channel_id}")]
            for channel in channels
        ]
        buttons.append([InlineKeyboardButton("➕ Добавить канал", callback_data="add_channel")])

        markup = InlineKeyboardMarkup(buttons)
        set_state(user_id, "start_menu")
        await client.send_message(chat_id=user_id, text=text, reply_markup=markup)


@Client.on_message(filters.private & filters.command("start"))
async def cmd_start(client: Client, message: Message):
    user = message.from_user
    async with async_session() as session:
        db_user = await get_user_by_id(session, user.id)
        if not db_user:
            await create_user(session, user.id, user.first_name)

    await send_start_message(client, user.id)
