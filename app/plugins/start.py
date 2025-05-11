from pyrogram import Client, filters
from pyrogram.types import Message
from app.db.session import async_session
from app.db.models import User
from app.db.crud.user import get_user, create_user


import logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def cmd_start(client: Client, message: Message):
    user = message.from_user
    first_name = message.from_user.first_name

    logger.info(f"User {first_name} started the bot.")

    async with async_session() as session:
        existing = await get_user(session, user.id)
        if not existing:
            await create_user(session, User(
                user_id=user.id,
                first_name=user.first_name,
            ))
    await message.reply(f"Привет, {first_name}!")



