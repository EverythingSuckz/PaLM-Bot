import logging
from bot import client, dp, palm
from aiogram import types, filters

from bot.database import add_user, clear_history

logger = logging.getLogger(__name__)


def check_bot_mentioned(message: types.Message, username: str):
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention" and (
                (entity.user and entity.user.id == client.id)
                or (username in message.text)
            ):
                return message.text[entity.offset : entity.offset + entity.length]
    return False


@dp.message_handler(
    filters.Command(commands=["clearhistory"], prefixes="!/", ignore_case=False)
)
async def clearhistory_cmd(message: types.Message):
    status = await message.answer(
        "<code>Please wait...</code>", parse_mode=types.ParseMode.HTML
    )
    await clear_history(message.from_id)
    await status.edit_text("<b>Done</b>.", parse_mode=types.ParseMode.HTML)
    add_user(
        message.from_user.id, message.from_user.full_name, message.from_user.username
    )


@dp.message_handler(filters.ContentTypeFilter(content_types=types.ContentType.TEXT))
@dp.throttled(
    lambda msg, loop, *args, **kwargs: loop.create_task(
        msg.answer("Too many messages, relax!", parse_mode=types.ParseMode.MARKDOWN)
    ),
    rate=1,
)
async def send_handler(message: types.Message):
    if message.chat.type in ("group", "supergroup"):
        if mentioned := check_bot_mentioned(message, (await client.me).username):
            logger.info(
                f"The bot was mentioned in {message.chat.title} by {message.from_user.first_name}"
            )
            text = message.text.replace(mentioned, "").strip()
        else:
            if not message.reply_to_message:
                return
            if not message.reply_to_message.from_user:
                return
            if not message.reply_to_message.from_user.id == client.id:
                return
            text = message.text
    elif message.chat.type == "private":
        text = message.text
    else:
        return
    if text and text.startswith("/"):
        return
    if not text:
        return
    await message.answer_chat_action("typing")
    user_id = message.from_id
    name = message.from_user.first_name if message.from_user else message.chat.title
    resp = await palm.get_reponse(user_id=user_id, name=name, message=text)
    if not resp:
        return logger.info("No reponse to %s's message", name)
    try:
        await message.reply(resp.last, parse_mode="Markdown")
    except Exception as e:
        logger.exception(e)
        await message.reply(resp.last)
    if message.chat.type == "private":
        add_user(
            message.from_id, message.from_user.full_name, message.from_user.username
        )
