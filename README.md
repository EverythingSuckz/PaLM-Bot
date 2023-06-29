# Serverless Aiogram Bot
A template for running your aiogram bots on serverless functions.


## Hosting
### Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone)

> **Note**: After deployment, Goto the `/updateWebhooks?token=\<your bot token\>`  path of your deployed app url to setup webhooks.
> An example will be https://bot-name.vercel.app/updateWebhooks?token=your-bot-token

### Environment Variables

- `BOT_TOKEN` - Your bot token
- `WEBHOOK_HOST` - Your webhook host url
- `PORT` - Port to run the server on (Default: 8000)
- `SERVERLESS` - Set to `true` if you are hosting on serverless functions (Default: `false`)

### Self Hosting

```bash
python -m bot
```

## Credits
- [aiogram](https://aiogram.dev/)
- [tg-serverless](https://github.com/illvart/tg-serverless)
- [fastapi-aiogram](https://github.com/malikovss/fastapi-aiogram)