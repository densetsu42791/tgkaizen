# plgs/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.crud import get_user_by_id, create_user, get_user_channels
from db.session import async_session
from utils.logger import logger
from utils.user_context import set_state


@Client.on_message(filters.private & filters.command("start"))
@Client.on_callback_query(filters.regex(r"^start$"))
async def start_handler(client: Client, event):
    # Определяем, что за тип события
    user_id = None
    if isinstance(event, Message):
        user_id = event.from_user.id
        logger.info(f"Получена команда /start от пользователя {user_id}")
    elif isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        logger.info(f"Нажата кнопка 'start' пользователем {user_id}")
        await event.answer()

    async with async_session() as session:
        db_user = await get_user_by_id(session, user_id)
        if not db_user:
            logger.info(f"Пользователь {user_id} не найден в базе. Создаю нового.")
            await create_user(session, user_id, event.from_user.first_name)
            db_user = await get_user_by_id(session, user_id)
        else:
            logger.info(f"Пользователь {user_id} найден: {db_user.first_name}")

        channels = await get_user_channels(session, user_id)
        logger.info(f"Найдено каналов у пользователя {user_id}: {len(channels)}")

    # Формируем сообщение и кнопки
    text = f"Hi, {db_user.first_name}"
    buttons = []

    for channel in channels:
        if isinstance(channel.channel_id, int):
            cb_data = f"get_info_channel:{channel.channel_id}"
            logger.info(f"Добавляю кнопку канала: {channel.title} -> {cb_data}")
            buttons.append([
                InlineKeyboardButton(text=channel.title, callback_data=cb_data)
            ])
        else:
            logger.warning(f"Некорректный channel_id: {channel.channel_id}")

    buttons.append([InlineKeyboardButton("➕ Добавить канал", callback_data="add_channel")])
    markup = InlineKeyboardMarkup(buttons)

    set_state(user_id, "start_menu")

    # Отправляем или редактируем сообщение
    if isinstance(event, Message):
        await client.send_message(chat_id=user_id, text=text, reply_markup=markup)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(text=text, reply_markup=markup)

