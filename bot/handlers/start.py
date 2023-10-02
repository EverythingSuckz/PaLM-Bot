import asyncio
from pyrogram import Client, filters, types, enums

from bot.helpers import limiter
from bot.database import add_user

gfn = lambda x: x.first_name + (f" {x.last_name}" if x.last_name else "")

@Client.on_message(filters.private, group=-1)
async def log_users(_, message: types.Message):
    asyncio.create_task(add_user(message.from_user.id, gfn(message.from_user), message.from_user.username))

@Client.on_message(filters.command("start") & filters.private)
@limiter(5)
async def start_cmd(_, message: types.Message):
    await message.reply(
        f"<b>Hi {message.from_user.mention(style=enums.ParseMode.HTML)}</b>. Send me something.",
        parse_mode=enums.ParseMode.HTML,
    )

@Client.on_message(filters.command("help") & filters.private)
@limiter(3)
async def help_cmd(_, message: types.Message):
    await message.reply(
        f"You can start a conversation with me by texting me <b>anything</b>. If you are looking for chat commands, type\n\n- /start - Get the start message.\n- /help - Get this same message.\n- /about - Get more info about the bot.\n- /clearhistory - Remove all your message history.\n\n<b>Have a great day!</b>", parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.command("about") & filters.private)
@limiter(5)
async def about_cmd(_, message: types.Message):
    markup = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text="What's PaLM?", url="https://t.me/wrenchies/226"),    
        types.InlineKeyboardButton(text="Source Code", url="https://github.com/EverythingSuckz/PaLM-bot"),
    ]])
    await message.reply(
        "I'm a <b>conversational bot</b> powerd by <b>Google's PaLM API</b>.",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=markup,
    )
