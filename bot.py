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
    # 1. Tepki ver
    try:
        await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji="👁️")])
    except:
        pass
    
    # 2. Bilgilendirme mesajı gönder
    status_msg = await update.message.reply_text("🔎 Aratılıyor ve indiriliyor...")
    
    file_path = "/tmp/media.mp3" if mode == "audio" else "/tmp/media.mp4"
    
    try:
        ydl_opts = {
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'cookiefile': 'cookies.txt',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        
        if mode == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best', 
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 
                'default_search': 'ytsearch1:'
            })
        else:
            ydl_opts.update({
                'format': 'best[ext=mp4]/best', 
                'default_search': 'ytsearch1:'
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
            
        if os.path.exists(file_path):
            await status_msg.edit_text("✅ İndirme tamamlandı, gönderiliyor...")
            if mode == "audio":
                await update.message.reply_audio(audio=open(file_path, 'rb'))
            else:
                await update.message.reply_video(video=open(file_path, 'rb'))
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Video bulunamadı.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Hata oluştu:\n{str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def start(update, context):
    await update.message.reply_text("Seba Downloader aktif!\n/search [isim] -> Video\n/indir [isim] -> MP3")

async def arama_video(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Lütfen bir isim yaz.")
        return
    await download_media(update, context, query, "video")

async def indir_sarki(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Lütfen bir isim yaz.")
        return
    await download_media(update, context, query, "audio")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", arama_video))
    app.add_handler(CommandHandler("indir", indir_sarki))
    app.run_polling()
