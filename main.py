from pyrogram import Client
import configparser
from db.database import init_db


config = configparser.ConfigParser()
config.read("config.ini")


api_id = int(config["pyrogram"]["api_id"])
api_hash = config["pyrogram"]["api_hash"]
bot_token = config["pyrogram"]["bot_token"]
plugins = dict(root=config["plugins"]["root"])


app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins)
app.run()  # ← просто запускаем без asyncio.run()



# async def main():
#     await init_db()
#     Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins).run()

# import asyncio
# asyncio.run(main())




#################################################################
# from pyrogram import Client, idle
# import configparser
# import asyncio
# config = configparser.ConfigParser()
# config.read("config.ini")
# api_id = int(config["pyrogram"]["api_id"])
# api_hash = config["pyrogram"]["api_hash"]
# bot_token = config["pyrogram"]["bot_token"]
# plugins = dict(root=config["plugins"]["root"])
# Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins).run()

###################################################################################
# app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins)
# async def startup():
#     await init_db()
#     await app.start()
#     print("Бот запущен. Для остановки нажми Ctrl+C")
#     await idle()
#     await app.stop()
# if __name__ == "__main__":
#     asyncio.run(startup())







