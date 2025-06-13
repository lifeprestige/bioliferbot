from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
import os
import openai

# Устанавливаем ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Клавиатура в Telegram
main_keyboard = ReplyKeyboardMarkup(
    [["📋 Начать автоворонку", "❓ Задать вопрос"]], resize_keyboard=True
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в BioLiferBot!\nЯ помогу подобрать добавки, улучшить самочувствие и ответить на любые вопросы.\n\nВыберите действие:",
        reply_markup=main_keyboard
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"[DEBUG] Получено сообщение: {user_message}")

    if user_message == "📋 Начать автоворонку":
        await update.message.reply_text("Отлично! Давайте начнем с простого вопроса: что вас сейчас больше всего беспокоит в здоровье?")

    elif user_message == "❓ Задать вопрос":
        await update.message.reply_text("Напишите свой вопрос, и я задам его GPT-4o…")

    else:
        await update.message.reply_text("⌛ Думаю над ответом…")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты — эксперт по биохакингу и нутрициологии."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
        except Exception as e:
            answer = f"Произошла ошибка при запросе к GPT: {e}"

        await update.message.reply_text(answer)

# Регистрация обработчиков
def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
