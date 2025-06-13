import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers.funnel_handlers import register_handlers
import logging

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://bioliferbot.onrender.com

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация приложения
app = Application.builder().token(BOT_TOKEN).build()

# Регистрируем обработчики
register_handlers(app)

# Запуск в режиме Webhook
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL  # Без /webhook в конце!
    )
