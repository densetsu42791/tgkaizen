import asyncio
from pyrogram import compose
import logging
from clients import create_bot, create_userbot
from services.user_info_userbot import set_userbot_client #new

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# async def main():
#     await compose([create_bot(), create_userbot()])
# asyncio.run(main())

async def main():
    bot = create_bot()
    userbot = create_userbot()

    # передаём userbot в сервис
    set_userbot_client(userbot)

    await compose([bot, userbot])

asyncio.run(main())













