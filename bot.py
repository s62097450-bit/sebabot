from telegram.ext import Application, CommandHandler
import yt_dlp
import os
from flask import Flask
from threading import Thread

TOKEN = "8834173312:AAF81dwqY15PJe8WIBfTjAEaQ69rJpgJzh0"

async def start_command(update, context):
    await update.message.reply_text("Seba Downloader Bot aktif! Linki yanıtlayıp /search yaz.")

async def search_command(update, context):
    replied_message = update.message.reply_to_message
    if not replied_message:
        await update.message.reply_text("Lütfen bir linki yanıtla.")
        return
    
    url = replied_message.text
    await update.message.reply_text("İndiriliyor...")
    
    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    await update.message.reply_video(video=open('video.mp4', 'rb'))
    os.remove('video.mp4')

app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot aktif!"

if __name__ == '__main__':
    Thread(target=lambda: app_web.run(host='0.0.0.0', port=10000)).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("search", search_command))
    app.run_polling()
import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.infinity_polling(skip_pending=True)
