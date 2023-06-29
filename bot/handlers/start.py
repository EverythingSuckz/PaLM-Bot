from bot import dp
from aiogram import types, filters

from bot.database import add_user


@dp.message_handler(
    filters.Command(commands=["start"], prefixes="!/", ignore_case=False)
)
async def start_cmd(message: types.Message):
    await message.answer(
        f"<b>Hi {message.from_user.get_mention(as_html=True)}</b>.",
        parse_mode=types.ParseMode.HTML,
    )
    add_user(
        message.from_user.id, message.from_user.full_name, message.from_user.username
    )


@dp.message_handler(
    filters.Command(commands=["help"], prefixes="!/", ignore_case=False)
)
async def help_cmd(message: types.Message):
    await message.answer(
        f"Just send me <b>anything</b>.", parse_mode=types.ParseMode.HTML
    )
    add_user(
        message.from_user.id, message.from_user.full_name, message.from_user.username
    )


@dp.message_handler(
    filters.Command(commands=["about"], prefixes="!/", ignore_case=False)
)
async def about_cmd(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            text="What's PaLM?", url="https://t.me/wrenchies/226"
        ),
        types.InlineKeyboardButton(
            text="Source Code", url="https://github.com/EverythingSuckz/PaLM-bot"
        ),
    )
    await message.answer(
        f"I'm a <b>conversational bot</b> powerd by <b>Google's PaLM API</b>.",
        parse_mode=types.ParseMode.HTML,
        reply_markup=markup,
    )
    add_user(
        message.from_user.id, message.from_user.full_name, message.from_user.username
    )
