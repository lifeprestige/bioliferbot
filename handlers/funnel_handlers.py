from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [
        ["🧠 Хочу улучшить здоровье", "❓ Задать вопрос"],
        ["💬 Хочу консультацию"]
    ],
    resize_keyboard=True
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в BioLiferBot!\nЯ помогу подобрать добавки, улучшить самочувствие и привести вас к лучшей версии себя.\n\nВыберите действие:",
        reply_markup=main_keyboard
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if user_message == "🧠 Хочу улучшить здоровье":
        await update.message.reply_text("Что именно вас сейчас беспокоит? Сон, энергия, пищеварение, либидо, стресс или что-то другое?")

    elif user_message == "❓ Задать вопрос":
        await update.message.reply_text("Напишите свой вопрос, и я кратко прокомментирую как специалист…")

    elif user_message == "💬 Хочу консультацию":
        await update.message.reply_text(
            "Отлично! Я предлагаю 3 формата консультаций:\n\n"
            "1️⃣ Быстрая консультация — 10–15 мин, подбор БАДов без анализов\n"
            "2️⃣ Глубокая консультация — с анализами и подробной стратегией\n"
            "3️⃣ Ведение — личная поддержка и регулярные корректировки\n\n"
            "Для начала, заполните короткую форму, чтобы я понял, как могу помочь:\n"
            "👉 https://docs.google.com/forms/d/e/1FAIpQLSdrkP3pR1ZhBkDLi15YiJCGDhJ0AbwjT9HqCsRRLXJVGUNeUg/viewform?usp=header"
        )

    else:
        await update.message.reply_text("⌛ Думаю над ответом…")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты — эксперт по биохакингу и нутрициологии. Отвечай с пользой, но мягко направляй к консультации."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            await update.message.reply_text(f"{answer}\n\nЕсли хотите индивидуальный подход — нажмите 💬 Хочу консультацию.")
        except Exception as e:
            await update.message.reply_text("Произошла ошибка при обработке запроса. Попробуйте позже.")

# Регистрируем обработчики
def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
