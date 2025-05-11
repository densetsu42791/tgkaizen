from pyrogram import Client
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


def create_bot():
    return Client(
        "bot",
        api_id=int(config["bot"]["api_id"]),
        api_hash=config["bot"]["api_hash"],
        bot_token=config["bot"]["bot_token"],
        plugins=dict(root=config["bot"]["plugins_root"]),
        workdir="sessions"
    )


def create_userbot():
    return Client(
        "userbot",
        api_id=int(config["userbot"]["api_id"]),
        api_hash=config["userbot"]["api_hash"],
        plugins=dict(root=config["userbot"]["plugins_root"]),
        workdir="sessions"
    )