# from pyrogram import Client
# import configparser


# config = configparser.ConfigParser()
# config.read("config.ini")


# def create_bot():
#     return Client(
#         "bot",
#         api_id=int(config["bot"]["api_id"]),
#         api_hash=config["bot"]["api_hash"],
#         bot_token=config["bot"]["bot_token"],
#         plugins=dict(root=config["bot"]["plugins_root"]),
#         workdir="sessions"
#     )


# def create_userbot():
#     return Client(
#         "userbot",
#         api_id=int(config["userbot"]["api_id"]),
#         api_hash=config["userbot"]["api_hash"],
#         plugins=dict(root=config["userbot"]["plugins_root"]),
#         workdir="sessions"
#     )

# clients.py

from pyrogram import Client
import configparser
from pathlib import Path


CONFIG_PATH = Path("config.ini")


def load_config() -> configparser.ConfigParser:
    """Загрузка конфигурации из файла config.ini."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


def create_bot() -> Client:
    """Создание экземпляра pyrogram-бота."""
    config = load_config()
    return Client(
        name="bot",
        api_id=int(config["bot"]["api_id"]),
        api_hash=config["bot"]["api_hash"],
        bot_token=config["bot"]["bot_token"],
        plugins={"root": config["bot"]["plugins_root"]},
        workdir="sessions",
    )


def create_userbot() -> Client:
    """Создание экземпляра pyrogram-пользовательского клиента."""
    config = load_config()
    return Client(
        name="userbot",
        api_id=int(config["userbot"]["api_id"]),
        api_hash=config["userbot"]["api_hash"],
        plugins={"root": config["userbot"]["plugins_root"]},
        workdir="sessions",
    )
