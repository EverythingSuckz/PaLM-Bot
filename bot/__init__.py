import logging
import sys

from pyrogram import Client

from config import Config
from bot.PaLM import PaLMChat

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

Bot: Client = None
palm = PaLMChat(Config.PALM_API_KEY)
