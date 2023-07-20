import asyncio
import logging
from pyrogram import Client, idle, types

from config import Config

async def main():
    import bot
    bot.Bot = bot = Client(
        "PaLM-Bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="bot/handlers"),
    )
    await bot.start()
    await bot.set_bot_commands(
        commands=[
            types.BotCommand("start", "Get the start message."),
            types.BotCommand("help", "Get this same message."),
            types.BotCommand("about", "Get more info about the bot."),
            types.BotCommand("clearhistory", "Remove all your message history."),
        ], scope=types.BotCommandScopeAllPrivateChats()
    )
    logging.info("Bot started as @%s.", bot.me.username)
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())