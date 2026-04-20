import os
import asyncio
import threading
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Настройки из переменных окружения Render ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# --- Простой веб-сервер для проверки работоспособности ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/health')
def health():
    return "OK", 200

def run_web_server():
    # Получаем порт, который выделил Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- Команды бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Привет! Бот работает.\nТвой ID: {update.effective_user.id}")

async def main_bot():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан!")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    logger.info("Бот запущен!")
    # Запускаем бота в режиме polling
    await application.run_polling()

def run_bot():
    asyncio.run(main_bot())

# --- Точка входа ---
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    threading.Thread(target=run_web_server).start()
    # Запускаем бота в главном потоке
    run_bot()
