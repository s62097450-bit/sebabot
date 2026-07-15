import os
import yt_dlp
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
    url = update.message.text
    
    if "http" not in url:
        await update.message.reply_text("Lütfen geçerli bir video bağlantısı (link) at.")
        return

    await update.message.reply_text("Video indiriliyor, lütfen bekle...")

    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024, # 50MB sınır (Telegram bot sınırı için)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video_file:
            await update.message.reply_video(video_file)
            
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text(f"İndirme başarısız oldu: {str(e)}")

def main():
    Thread(target=run_web, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot video indirmeye hazır...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
