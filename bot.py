import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для анализа тональности текста. Отправьте мне любое сообщение.")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    logger.info(f"Received: {text}")
    try:
        response = requests.post(API_URL, json={"text": text}, timeout=10)
        data = response.json()
        label = data.get("label", "unknown")
        confidence = data.get("confidence", 0.0)
        sentiment = "ПОЗИТИВНАЯ" if label == "positive" else "НЕГАТИВНАЯ"
        reply = f"Тональность: {sentiment} (уверенность: {confidence:.2f})"
        update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("Ошибка обработки")

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set")
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    logger.info("Бот запущен и ожидает сообщения...")
    updater.idle()

if __name__ == "__main__":
    main()