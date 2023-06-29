import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SERVERLESS = os.getenv("SERVERLESS", "").lower() in ("yes", "y", "1", "true")
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    PORT = int(os.getenv("PORT", 8080))