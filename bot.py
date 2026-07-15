import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mesaj alındı!")

def main():
    Thread(target=run_web, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot çalışıyor...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
