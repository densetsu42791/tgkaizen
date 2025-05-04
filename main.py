import asyncio
from pyrogram import Client, compose
import configparser
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
config = configparser.ConfigParser()
config.read("config.ini")

bot_api_id = int(config["bot"]["api_id"])
bot_api_hash = config["bot"]["api_hash"]
bot_token = config["bot"]["bot_token"]
bot_plugins = dict(root=config["bot"]["plugins_root"])

user_api_id = int(config["userbot"]["api_id"])
user_api_hash = config["userbot"]["api_hash"]
user_plugins = dict(root=config["userbot"]["plugins_root"])


async def main():
    apps = [
        Client("bot", api_id=bot_api_id, api_hash=bot_api_hash, bot_token=bot_token, plugins=bot_plugins),
        Client("userbot", api_id=user_api_id, api_hash=user_api_hash, plugins=user_plugins)
    ]
    await compose(apps)
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








