import bot
from api import app
from config import Config
from fastapi.responses import JSONResponse

@app.get("/updateWebhooks")
async def root_endpoint(token: str):
    if token != Config.BOT_TOKEN:
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    return await bot.client.set_webhook(
                url=bot.WEBHOOK_URL,
                allowed_updates=bot.ALLOWED_UPDATES
            )