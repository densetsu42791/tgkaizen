import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/bot.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
