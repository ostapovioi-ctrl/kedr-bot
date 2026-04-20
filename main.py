import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Привет! Бот работает.\nТвой ID: {update.effective_user.id}")

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
