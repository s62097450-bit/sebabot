import logging
import os
import threading
import yt_dlp
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Online", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seba Downloader aktif!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text or not text.startswith("http"):
        return 

    status_msg = await update.message.reply_text("İndiriliyor... ⏳")
    file_path = "/tmp/video.mp4"
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
            
        if os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, 'rb'))
        else:
            await update.message.reply_text("İndirme başarısız oldu. Linki kontrol et.")
            
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        try:
            await status_msg.delete()
        except:
            pass

if __name__ == '__main__':
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
