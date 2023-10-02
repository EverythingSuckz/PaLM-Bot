import re
import logging
from typing import List

from pyrogram import enums, types, filters
from google.generativeai.types.safety_types import ContentFilterDict

from bot import Bot, palm
from bot.database import clear_history
from bot.helpers import limiter, mentioned

logger = logging.getLogger(__name__)

gfn = lambda x: f"{x.first_name} {x.last_name}" if x.last_name else ""

@Bot.on_message(filters.command("clearhistory") & filters.private)
@limiter(15)
async def clearhistory_cmd(_, message: types.Message):
    status = await message.reply(
        "<code>Please wait...</code>", parse_mode=enums.ParseMode.HTML
    )
    await clear_history(message.from_user.id if message.from_user else message.sender_chat.id)
    await status.edit_text("<b>Done</b>.", parse_mode=enums.ParseMode.HTML)
    


@Bot.on_message((filters.text & filters.private) | (filters.text & mentioned & filters.group) & filters.incoming, group=2)
@limiter(3)
async def send_handler(_, message: types.Message):
    text = re.sub(f"@{Bot.me.username}", "", message.text, flags=re.IGNORECASE).strip()
    text = message.text.strip()
    if text and text.startswith("/"):
        return
    if not text:
        return
    await message.reply_chat_action(enums.ChatAction.TYPING)
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    name = message.from_user.first_name if message.from_user else message.sender_chat.title
    resp = await palm.get_reponse(user_id=user_id, name=name, message=text)
    if not resp:
        await message.reply("<i>*AI did not repond*</i>")
        return logger.info("No reponse to %s's message", name)
    if not resp.last:
        filers: List[ContentFilterDict] = resp.filters
        await message.reply("<i>*ignores you*</i>")
        logger.info("No reponse to %s's message", name)
        if filers:
            logger.info("Due to the following filters:")
            for fil in filers:
                logger.info(f"\t[%s]: %s", fil.get("reason"), fil.get("message"))
        return
    try:
        await message.reply(resp.last, parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True, quote=True)
    except Exception as e:
        logger.exception(e, stack_info=True)
        await message.reply(resp.last, disable_web_page_preview=True, quote=True)
