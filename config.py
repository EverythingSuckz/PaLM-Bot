import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SERVERLESS = os.getenv("SERVERLESS", "").lower() in ("yes", "y", "1", "true")
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    PORT = int(os.getenv("PORT", 8080))
    PALM_API_KEY = os.getenv("PALM_API_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
