# from pyrogram import filters
# from pyrogram.types import CallbackQuery
# from pyrogram.handlers import CallbackQueryHandler
# from app.db.session import async_session
# from app.db.crud import add_many_subscribers
# from app.logger import logger

# userbot_client = None  # экземпляр Client

# def set_userbot_client(client):
#     global userbot_client
#     userbot_client = client
#     # Регистрируем обработчик сразу после получения клиента
#     userbot_client.add_handler(
#         CallbackQueryHandler(parse_subscribers_handler, filters.regex(r"parse_subscribers:.*"))
#     )


# async def parse_subscribers_handler(client, callback: CallbackQuery):
#     channel_id = int(callback.data.split(":")[1])
#     user_id = callback.from_user.id

#     try:
#         if not userbot_client:
#             await callback.message.edit_text("❌ Userbot не инициализирован.")
#             return

#         if not userbot_client.is_connected:
#             await userbot_client.start()

#         subscribers = []

#         async for member in userbot_client.get_chat_members(channel_id):
#             sub_data = {
#                 "user_id": member.user.id,
#                 "first_name": member.user.first_name,
#                 "phone_number": getattr(member.user, "phone_number", None),
#                 "channel_id": channel_id,
#             }
#             subscribers.append(sub_data)

#         async with async_session() as session:
#             await add_many_subscribers(subscribers, session)

#         await callback.message.edit_text("✅ Подписчики успешно добавлены в базу данных.")
#         await callback.answer()

#     except Exception as e:
#         logger.error(f"Ошибка при парсинге подписчиков: {e}")
#         await callback.message.edit_text("❌ Произошла ошибка при парсинге подписчиков.")
#         await callback.answer()
