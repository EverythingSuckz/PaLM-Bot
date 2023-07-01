# PaLM Telegram Bot
A small bot that interacts with Google's PaLM Chat API and can be hosted on serverless functions.

> Looking for the fast pyrogram version? <br>
Check out [this](https://github.com/EverythingSuckz/PaLM-Bot/tree/pyrogram) branch.

# Demo
A working demo can be found at [@NotAIChatBot](https://telegram.dog/NotAIChatBot).

# Requirements

#### Python 3.8+
Install Python 3.8 or higher from [here](https://www.python.org/downloads/)
#### PostgreSQL Database
Install PostgreSQL from [here](https://www.postgresql.org/download/) or use a managed database service like [ElephantSQL](https://www.elephantsql.com/)
#### PaLM API Key
Get your PaLM API key from [here](https://makersuite.google.com/)

# Environment Variables

- `BOT_TOKEN` - Your bot token
- `WEBHOOK_HOST` - Your webhook host url
- `PORT` - Port to run the server on (Default: 8000)
- `SERVERLESS` - Set to `true` if you are hosting on serverless functions (Default: `false`)
- `PALM_API_KEY` - Your PaLM API key
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_NAME` - Database name

# Hosting
## Vercel (Pro Plan)

> **Note:** You can use the free plan but the max execution time is 10 seconds which is not enough for big reponses from the API.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FEverythingSuckz%2FPaLM-Bot&env=BOT_TOKEN,WEBHOOK_HOST,PALM_API_KEY,DB_USER,DB_PASSWORD,DB_HOST,DB_NAME&envDescription=Check%20out%20the%20readme%20for%20info&envLink=https%3A%2F%2Fgithub.com%2FEverythingSuckz%2FPaLM-Bot%23environment-variables&demo-title=PaLM%20Telegram%20Chat%20Bot&demo-description=A%20small%20bot%20that%20interacts%20with%20Google's%20PaLM%20Chat%20API%20and%20can%20be%20hosted%20on%20serverless%20functions.&demo-url=https%3A%2F%2Ftelegram.dog%2FNotAIChatBot)

### Post Deployment Steps
If you've hosted it on webhooks (serverless) then after deployment, Goto the `/updateWebhooks?token=your-bot-token`  path of your deployed app url to setup webhooks.
> An example will be https://bot-name.vercel.app/updateWebhooks?token=your-bot-token

# Self Hosting

```bash
git clone -b aiogram https://github.com/EverythingSuckz/PaLM-Bot
cd PaLM-Bot
pip install -r requirements.txt
python -m bot
```

_Generated from [Aiogram Serverless Bot](https://github.com/EverythingSuckz/aiogram-serverless-bot)._

**Give a ⭐ if you like this project!**