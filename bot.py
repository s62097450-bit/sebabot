import logging
import os
import threading
import yt_dlp
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Online", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

logging.basicConfig(level=logging.INFO)

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE, query, mode):
    # Senin mesajına göz emojisi ile tepki ver
    try:
        await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji="👁️")])
    except Exception:
        pass # Eğer tepki veremezse botun yetkisi yok demektir, hata vermemesi için geçtik.

    file_path = "/tmp/media.mp3" if mode == "audio" else "/tmp/media.mp4"
    
    try:
        ydl_opts = {
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'cookiefile': 'cookies.txt',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        
        if mode == "audio":
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'default_search': 'ytsearch1:'})
        else:
            ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'default_search': 'ytsearch1:'})
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
            
        if os.path.exists(file_path):
            if mode == "audio":
                await update.message.reply_audio(audio=open(file_path, 'rb'))
            else:
                await update.message.reply_video(video=open(file_path, 'rb'))
        else:
            await update.message.reply_text("İçerik bulunamadı veya platform engelledi.")
            
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def start(update, context):
    await update.message.reply_text("Seba Downloader aktif!\n/indir [isim] -> MP3\n/search [isim] -> Video")

async def handle_message(update, context):
    text = update.message.text
    if text and text.startswith("http"):
        await download_media(update, context, text, "video")

async def indir_sarki(update, context):
    query = " ".join(context.args)
    if not query: return
    await download_media(update, context, query, "audio")

async def arama_video(update, context):
    query = " ".join(context.args)
    if not query: return
    await download_media(update, context, query, "video")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("indir", indir_sarki))
    app.add_handler(CommandHandler("search", arama_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
