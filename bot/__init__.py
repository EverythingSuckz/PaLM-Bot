import logging
from urllib.parse import urljoin

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import Config

WEBHOOK_PATH = f"/api/bot/{Config.BOT_TOKEN}"
WEBHOOK_URL = urljoin(Config.WEBHOOK_HOST, WEBHOOK_PATH)
ALLOWED_UPDATES = ["message", "callback_query", "inline_query"]


logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
)

client = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(client, storage=storage)
dp.middleware.setup(LoggingMiddleware())