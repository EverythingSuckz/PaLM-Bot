# PaLM Telegram Bot
A telegram bot that interacts with Google's PaLM Chat API and can be hosted on serverless functions.

> Looking for serverless verson based on aiogram? <br>
> Check out [this](https://github.com/EverythingSuckz/PaLM-Bot/tree/aiogram) branch.

# Demo
A working demo can be found at [@NotAIChatBot](https://telegram.dog/NotAIChatBot).

# Requirements

#### Telegram API ID and Hash
Get your API ID and Hash from [my.telegram.org](https://my.telegram.org).
#### Telegram Bot API Token
Create a bot and get the bot token from [@BotFather](https://telegram.dog/BotFather).
#### Python 3.8+
Install Python 3.8 or higher from [here](https://www.python.org/downloads/)
#### PostgreSQL Database
Install PostgreSQL from [here](https://www.postgresql.org/download/) or use a managed database service like [ElephantSQL](https://www.elephantsql.com/)
#### PaLM API Key
Get your PaLM API key from [here](https://makersuite.google.com/)

# Environment Variables

- `API_ID` - Your [API ID](#telegram-api-id-and-hash)
- `API_HASH` - Your [API Hash](#telegram-api-id-and-hash)
- `BOT_TOKEN` - Your [bot token](#telegram-bot-api-token)
- `PALM_API_KEY` - Your [PaLM API key](#palm-api-key)
- `DB_USER` - [Database](#postgresql-database) username
- `DB_PASSWORD` - [Database](#postgresql-database) password
- `DB_HOST` - [Database](#postgresql-database) host
- `DB_NAME` - [Database](#postgresql-database) name

# Hosting
# Self Hosting

```bash
git clone -b pyrogram https://github.com/EverythingSuckz/PaLM-Bot
cd PaLM-Bot
python3 -m venv venv
source venv/bin/activate # Linux
.\venv\Scripts\activate # Windows
pip install -r requirements.txt
python -m bot
```

_Based on [pyrogram](https://github.com/pyrogram/pyrogram)._

**Give a ⭐ if you like this project!**