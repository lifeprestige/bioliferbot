import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers.funnel_handlers import register_handlers
import logging
from fastapi import FastAPI, Request
import uvicorn

# Загрузка переменных
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8000))

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Инициализация бота и FastAPI
app = Application.builder().token(BOT_TOKEN).build()
register_handlers(app)

fastapi_app = FastAPI()

@fastapi_app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = app.update_queue._update_class.de_json(data, app.bot)
    await app.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    app.bot.set_webhook(WEBHOOK_URL)
    uvicorn.run(fastapi_app, host="0.0.0.0", port=PORT)
