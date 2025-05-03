from pyrogram import Client
import configparser
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
config = configparser.ConfigParser()
config.read("config.ini")


api_id = int(config["pyrogram"]["api_id"])
api_hash = config["pyrogram"]["api_hash"]
bot_token = config["pyrogram"]["bot_token"]
plugins = dict(root=config["plugins"]["root"])


app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins)
app.run()








