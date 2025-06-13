import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from handlers.funnel_handlers import register_handlers

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Регистрируем обработчики
register_handlers(telegram_app)

@app.on_event("startup")
async def startup():
    await telegram_app.initialize()  # ✅ добавлено
    await telegram_app.start()       # ✅ добавлено
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("Webhook установлен!")

@app.on_event("shutdown")
async def shutdown():
    await telegram_app.stop()
    await telegram_app.shutdown()

@app.post("/webhook")
async def process_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
