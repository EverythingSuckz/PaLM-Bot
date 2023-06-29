import logging
from fastapi import FastAPI
from aiogram import types

import bot
from config import Config
logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)


@app.on_event("startup")
async def on_startup():
    logger.info("Startup")
    await bot.client.set_my_commands([types.BotCommand(command="/start", description="Start the bot")])
    if Config.SERVERLESS:
        webhook_info = await bot.client.get_webhook_info()
        if (webhook_info.url != bot.WEBHOOK_URL) or (webhook_info.allowed_updates != bot.ALLOWED_UPDATES):
            await bot.client.set_webhook(
                url=bot.WEBHOOK_URL,
                allowed_updates=bot.ALLOWED_UPDATES
            )


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutdown")
    if Config.SERVERLESS is True:
        await bot.client.delete_webhook()
    await bot.storage.close()
    await bot.storage.wait_closed()
    await bot.client.session.close()