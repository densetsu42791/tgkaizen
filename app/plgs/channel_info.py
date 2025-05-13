from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.session import async_session
from app.db.crud import get_channel_by_id
from app.plgs.start import send_start_message
from app.logger import logger


@Client.on_callback_query(filters.regex(r"get_info_channel:.*"))
async def channel_info_handler(client: Client, callback: CallbackQuery):
    channel_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with async_session() as session:
        channel = await get_channel_by_id(session, channel_id)
        if not channel:
            await callback.answer("Канал не найден.", show_alert=True)
            return

        text = (
            f"✅ Канал <b>{channel.title}</b> успешно подключен.\n"
            f"<code>channel_id: {channel.channel_id}</code>\n"
            f"👥 start_count: {channel.start_count_subs or 0}"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Спарсить подписчиков", callback_data="test")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ])

        await callback.message.edit_text(text, reply_markup=buttons)
        await callback.answer()


@Client.on_callback_query(filters.regex(r"^start$"))
async def start_menu_handler(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    await send_start_message(client, user_id)
