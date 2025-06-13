import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers.funnel_handlers import register_handlers
import logging

# Загрузка переменных из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация приложения
app = Application.builder().token(BOT_TOKEN).build()

# Регистрируем обработчики
register_handlers(app)

# Webhook-режим (для Render)
if __name__ == "__main__":
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например, https://bioliferbot.onrender.com/webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}"
    )
