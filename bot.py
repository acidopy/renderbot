import logging
import os
import requests
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
BASE_URL = "https://api.bybit.com"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot de arbitraje activo. Enviá /arbitraje para comenzar.")

async def arbitraje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"{BASE_URL}/v5/market/tickers?category=spot"
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.text.startswith("{"):
            await update.message.reply_text("✅ Datos de Bybit obtenidos correctamente.")
        else:
            await update.message.reply_text(f"❌ Error {response.status_code}: Bybit bloqueó la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error al conectar: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("arbitraje", arbitraje))
    loop = asyncio.get_event_loop()
    app.run_polling()

if __name__ == "__main__":
    main()
