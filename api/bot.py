from api import app
from aiogram import types, Dispatcher, Bot

import bot.handlers
from bot import WEBHOOK_PATH, dp, client

@app.post(WEBHOOK_PATH)
async def bot_webhooks_endpoint(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(client)
    await dp.process_update(telegram_update)