import asyncio
from pyrogram import Client
import configparser
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

config = configparser.ConfigParser()
config.read("config.ini")

# Настройки бота
bot_api_id = int(config["bot"]["api_id"])
bot_api_hash = config["bot"]["api_hash"]
bot_token = config["bot"]["bot_token"]
bot_plugins = dict(root=config["bot"]["plugins_root"])

# Настройки юзер-бота
user_api_id = int(config["userbot"]["api_id"])
user_api_hash = config["userbot"]["api_hash"]
user_session_name = config["userbot"]["session_name"]
user_plugins = dict(root=config["userbot"]["plugins_root"])

# 🟢 Бот-клиент
bot_app = Client(
    "bot",
    api_id=bot_api_id,
    api_hash=bot_api_hash,
    bot_token=bot_token,
    plugins=bot_plugins
)

# 🔵 Юзер-бот-клиент (использует другой session_name)
user_app = Client(
    user_session_name,
    api_id=user_api_id,
    api_hash=user_api_hash,
    plugins=user_plugins  # отдельная папка для плагинов юзер-бота
)

async def main():
    await bot_app.start()
    await user_app.start()
    logging.info("🤖 Бот и 👤 Юзер-бот запущены.")
    await asyncio.Event().wait()  # бесконечное ожидание

if __name__ == "__main__":
    asyncio.run(main())







# from pyrogram import Client
# import configparser
# import logging


# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
# config = configparser.ConfigParser()
# config.read("config.ini")


# api_id = int(config["pyrogram"]["api_id"])
# api_hash = config["pyrogram"]["api_hash"]
# bot_token = config["pyrogram"]["bot_token"]
# plugins = dict(root=config["plugins"]["root"])


# app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins)
# app.run()








