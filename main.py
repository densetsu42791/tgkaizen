import asyncio
from pyrogram import compose
import logging
from clients import create_bot, create_userbot
from src.parse import set_userbot_client
from src.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


async def main():

    bot = create_bot()
    userbot = create_userbot()
    
    start_scheduler(bot)
    set_userbot_client(userbot)
    
    #await compose([bot])
    await compose([bot, userbot])

asyncio.run(main())

